import React from 'react'

var PatronForm = React.createClass({
  render(){
    return (
      <div className='patron-form'>
        <label>Patron ID</label>
        <input type='text' name='patron-id'/>
      </div>
    );
  },
});
