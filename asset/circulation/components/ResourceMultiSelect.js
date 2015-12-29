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
            value: '',
        };
    },
    getResources(input, callback){
        input = input.toLowerCase();

        setTimeout(function() {
            var options = [
                { value: 'one', label: 'One' },
                { value: 'two', label: 'Two' },
                { value: '3', label: 'Three' }
            ];
            callback(null, {

                options: options,
                // CAREFUL! Only set this to true when there are no more options,
                // or more specific queries will not be sent to the server.
                complete: true
            });
        }, 500);
    },
    render(){
        return (
            <div className="section">
                <label htmlFor="resource-select">Resources</label>
                <Select.Async
                    value={this.state.value}
                    loadOptions={this.getResources}
                    onChange={this.handleSelectChange} />
            </div>
        );
    }

});

module.exports = ResourceSelectField;
