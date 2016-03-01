import React from 'react'
import PatronPanel from './PatronPanel.react'
import ResourcePanel from './ResourcePanel.react'

var OneStopApp = React.createClass({
  render(){
    return (
      <div className='onestop grid'>
        <PatronPanel />
        <ResourcePanel />
      </div>
    );
  },
});

module.exports = OneStopApp;
