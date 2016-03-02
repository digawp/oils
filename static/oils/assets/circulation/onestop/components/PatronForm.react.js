import React from 'react'
import PatronActionCreators from '../actions/PatronActionCreators'


var PatronForm = React.createClass({
  getInitialState(){
    return {patron_id: ''};
  },

  _onChange(e){
    this.setState({patron_id: e.target.value});
  },

  _onKeyPress(e){
    if (e.key === 'Enter'){
      e.preventDefault();
      var patron_id = this.state.patron_id.trim();
      if (patron_id){
        PatronActionCreators.lookupPatron(patron_id);
      }
    }
  },

  render(){
    return (
      <div className='patron-form'>
        <label>Patron ID</label>
        <input type='text' name='patron-id'
          onChange={this._onChange}
          onKeyPress={this._onKeyPress} 
          value={this.state.patron_id} />
      </div>
    );
  },
});

module.exports = PatronForm;
