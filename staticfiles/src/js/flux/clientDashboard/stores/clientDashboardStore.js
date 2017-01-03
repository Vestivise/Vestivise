/**
 * Created by raylenmargono on 12/6/16.
 */
import {DataSource} from 'js/flux/clientDashboard/sources/sources';
import {ClientDataAction, ClientAppAction} from 'js/flux/clientDashboard/actions/actions';
import { datasource, bind, createStore } from 'alt-utils/lib/decorators';
import alt from 'js/flux/alt';
import ModuleStack from './ModuleStack';
import Module from './Module';

class DashboardStore{

    constructor(moduleAPI){
        this.moduleAPI = moduleAPI;
    }

    getState(){
        return {
            isLoading: false,
            profileFetchError : false,
            moduleFetchError : false,
            user: {},
            isCompleted : false,
            isLinked : false,
            notifications : {},
            moduleStacks : {
                Asset : new ModuleStack("Asset"),
                Return : new ModuleStack("Return"),
                Risk: new ModuleStack("Risk"),
                Cost : new ModuleStack("Cost")
            },
            navElement : null
        };
    }

    bindAppListeners(){
        this.bindListeners({
            loadingResults : ClientDataAction.loadingResults,
            recievedProfileResults : ClientDataAction.recievedProfileResults,
            fetchingProfileResultsFailed : ClientDataAction.fetchingProfileResultsFailed,
            recievedModuleResults : ClientDataAction.recievedModuleResults,
            fetchingModuleResultsFailed : ClientDataAction.fetchingProfileResultsFailed,
            nextModule : ClientAppAction.nextModule,
            prevModule : ClientAppAction.prevModule,
            renderNewNavEl : ClientAppAction.renderNewNavElement
        });
    }

    renderNewNavEl(el){
        this.setState({
            navElement : el
        });
    }

    nextModule(category){
        const moduleStacks = this.state.moduleStacks;
        const stack = moduleStacks[category];
        stack.next();
        this.setState({
           moduleStacks : moduleStacks
        });
    }

    prevModule(category){
        const moduleStacks = this.state.moduleStacks;
        const stack = moduleStacks[category];
        stack.prev();
        this.setState({
           moduleStacks : moduleStacks
        });
    }

    loadingResults(){
        this.setState({
            isLoading: true
        });
    }

    recievedProfileResults(data){
        const result = data['data'];

        var moduleStacks = this.state.moduleStacks;

        result["modules"].forEach(function(moduleRequest){
            const category = moduleRequest["category"];
            const moduleName = moduleRequest["name"];
            const moduleEndpoint = moduleRequest["endpoint"];

            const module = new Module(moduleName, moduleEndpoint, category);
            const stack = moduleStacks[category];
            stack.pushModule(module);
        });

        this.setState({
            user : {
                firstName : result["firstName"],
                lastName : result["lastName"],
                company : result["company"]
            },
            isCompleted : result["isCompleted"],
            isLinked : result["isLinked"],
            notifications : result["notification"],
            moduleStacks : moduleStacks,
            isLoading : false
        });
        if(result["isCompleted"] && result["isLinked"]){
            for(var key in moduleStacks){
                const list = moduleStacks[key].getList();
                list.forEach(function(module){
                    ClientDataAction.fetchModule(module, this.moduleAPI);
                }.bind(this))
            }
        }
    }

    fetchingProfileResultsFailed(data){
        this.setState({
           profileFetchError: true
        });
    }

    recievedModuleResults(payload){
        const data = payload["data"];
        const module = payload["module"];
        var moduleStacks = this.state.moduleStacks;
        const stack = moduleStacks[module.getCategory()];
        stack.updateData(module, data);
        moduleStacks[module.getCategory()] = stack;
        this.setState({
            moduleStacks : moduleStacks
        });
    }


    fetchingModuleResultsFailed(data){
        this.setState({
           moduleFetchError: true
        });
    }

}

@datasource(DataSource)
class DemoDashboardStore extends DashboardStore{
    constructor(){
        super(Urls.demoData);
        this.state = this.getState();
        this.state["profileAPIURL"] = Urls.demoProfile;
        this.state["isDemo"] = true;

        this.bindAppListeners();
    }
}

@datasource(DataSource)
class ClientDashboardStore extends DashboardStore{
    constructor(){
        super(Urls.broker);
        this.state = this.getState();
        this.state["profileAPIURL"] = Urls.profile;
        this.state["isDemo"] = false;

        this.bindAppListeners();
    }
}

export {ClientDashboardStore, DemoDashboardStore};