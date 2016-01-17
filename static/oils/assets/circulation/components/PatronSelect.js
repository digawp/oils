import React from 'react'
import Select from 'react-select'

var PatronSelectField = React.createClass({
    displayName: 'PatronSelectField',
    handleSelectChange(value){
        console.log("You've selected: ", value);
        this.setState({value});
    },
    getInitialState(){
        return {
            value: '',
            name: 'patron_username'
        };
    },
    getPatrons(input){
        input = input.toLowerCase();
        return fetch(`/api/patrons/?username=${input}`)
            .then((response)=>{
                return response.json();
            }).then((json)=>{
                var options = json.map((data)=>{
                    return {
                        value: data.username,
                        label: data.username + " (" + data.email + ")",
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
                <label htmlFor="patron-select">Patron</label>
                <Select.Async
                    name={this.state.name}
                    value={this.state.value}
                    multi={false}
                    loadOptions={this.getPatrons}
                    onChange={this.handleSelectChange} />
            </div>
        );
    }

});

module.exports = PatronSelectField;
