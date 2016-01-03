import React from 'react'
import Select from 'react-select'

var ResourceSelectField = React.createClass({
    displayName: 'ResourceSelectField',
    handleSelectChange(value){
        console.log("You've selected: ", value);
        this.setState({value});
    },
    getInitialState(){
        return {
            name: 'resource_identifier',
            value: '',
        };
    },
    getResources(input){
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
                    name={this.state.name}
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
