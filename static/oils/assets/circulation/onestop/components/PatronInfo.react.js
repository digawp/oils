import React from 'react'
import PatronStore from '../stores/PatronStore'

function getStateFromStores(){
  return {
    patron: PatronStore.get(),
  }
}

var PatronInfo = React.createClass({
  getInitialState(){
    return getStateFromStores();
  },
  componentDidMount(){
    PatronStore.addChangeListener(this._onChange);    
  },
  componentWillUnmount(){
    PatronStore.removeChangeListener(this._onChange);    
  },
  render(){
    var info;
    if (this.state.patron.id){
      info = <div>
        ID: {this.state.patron.id}<br/>
        Name: {this.state.patron.name}<br/>
        Address: {this.state.patron.address}<br/>
        Loan Limit: {this.state.patron.loan_limit}
      </div>;
    } else {
      info = '';
    }
    return (
      <div className='patron-info'>
        {info}
      </div>
    );
  },

  _onChange(){
    this.setState(getStateFromStores());
  },
});

module.exports = PatronInfo
