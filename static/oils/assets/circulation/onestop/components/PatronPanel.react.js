import React from 'react'
import PatronForm from './PatronForm.react'
import PatronInfo from './PatronInfo.react'


var PatronPanel = React.createClass({
  render(){
    return (
      <div className='patron-panel'>
        <PatronForm />
        <PatronInfo />
      </div>
    );
  },
});

module.exports = PatronPanel;
