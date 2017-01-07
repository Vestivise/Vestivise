/**
 * Created by raylenmargono on 12/15/16.
 */
import React, {Component} from 'react';
import Highcharts from 'highcharts';


var config = {};

config.title = {
  text: '',
  style: {
    color : "#000000"
  }
};

config.chart = {
    type: 'area',
    backgroundColor: null,
}

config.xAxis = {
    tickmarkPlacement: 'on',
    title: {
        enabled: false
    },
    labels: {
        enabled: true,
        formatter: null
    },
    startOnTick: false,
    endOnTick: false,
    minPadding: 0,
    maxPadding: 0,
}

config.yAxis = {
    title: {
        text: '',
        style: {
            color : "#434778"
        }
    },
    gridLineColor: 'white',
    labels: {
        style: {
            color : '#434778'
        }
    },
}

config.plotOptions = {
    area: {
        lineColor: '#666666',
        lineWidth: 1,
        marker: {
            enabled: false,
            symbol: 'circle',
            radius: 2,
            states: {
                hover: {
                    enabled: true
                }
            }
        },
        pointStart : 0
    },
    series : {
        fillOpacity: 1
    }
}

config.credits = {
    enabled: false
};

config.tooltip =  {
    formatter: null
}

config.series = [];

class VestiAreaLine extends Component{

    constructor(props){
        super(props);
    }

    renderChart(){
        const payload = this.props.payload;
        config.series = payload.data;
        config.yAxis.title.text = payload.yTitle;
        config.tooltip.formatter = payload.formatter;
        config.xAxis.labels.formatter = function () {
            return payload.categories[this.value];
        };
        Highcharts.chart(this.props.name, config);
    }

    componentDidMount(){
        this.renderChart();
    }


    render(){
        return(<div className="vestiAreaLine" id={this.props.name}></div>);
    }

}


export default VestiAreaLine;