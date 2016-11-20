import React from 'react';
import ModuleFactory from '../factories/moduleFactory.jsx';
import AppActions from '../../../js/flux/actions/dashboard/dashboardActions';
import { StackConst } from '../../../js/const/stack.const';

class RiskStack extends React.Component {
    constructor(props) {
        super(props);
        this.displayName = 'RiskStack';
    }

    getCurrentModule(){
        const stack = this.props.data;
        const currentModule = stack.getCurrentModule();

        if(currentModule){
            const name = currentModule.getModuleID();
            var endpoint = currentModule.getEndPoint();

            if(this.props.isDemo){
                endpoint  = endpoint + "Test";
            }

            return ModuleFactory.createModule(name, endpoint);
        }
        return null;
    }

    animate(){
        const stack = this.props.data;
        const currentModule = stack.getCurrentModule();
        console.log(this.props.topRowHeight);
        AppActions.animate(StackConst.RISK, currentModule.getModuleID(), currentModule.getName(), this.props.topRowHeight);
    }

    render() {
        return (
        	<div onClick={this.animate.bind(this)}>
                { this.getCurrentModule() }
				<p id="t1" className="modTitle R">Risks</p>
			</div>
        );
    }
}

export default RiskStack;
