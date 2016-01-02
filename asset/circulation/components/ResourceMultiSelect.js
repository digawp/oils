import React from 'react'
import Select from 'react-select'

var ResourceSelectField = React.createClass({
    displayName: 'ResourceSelectField',
    isLoading: true,
    handleSelectChange(value){
        console.log("You've selected: ", value);
        this.setState({value});
    },
    getInitialState(){
        return {
            value: '',
        };
    },
    getResources(input){
        if (input === ''){
            return [];
        }

        input = input.toLowerCase();

        // API call
        return fetch(`/api/resources/?code=${input}`)
            .then((response)=>{
                return response.json();
            }).then((json)=>{
                var options = json.map((data)=>{
                    return {
                        value: data.code,
                        label: data.code + " (" + data.title + ")",
                    };
                });
                return {
                    options: options,
                };
            });
    },
    render(){
        return (
            <div className="section">
                <label htmlFor="resource-select">Resources</label>
                <Select.Async
                    value={this.state.value}
                    multi={true}
                    isLoading={false}
                    loadOptions={this.getResources}
                    onChange={this.handleSelectChange} />
            </div>
        );
    }

});

module.exports = ResourceSelectField;
