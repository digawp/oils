/*
import 'babel-polyfill'
import React, { Component } from 'react'
import ReactDOM from 'react-dom'

import Select from 'react-select'
import 'react-select/less/default.less'


class LookupForm extends Component {
  constructor (props) {
    super(props);
    this.state = {
      identifiers: [
        {value: 'isbn', label: '1'},
        {value: 'lccn', label: '2'},
        {value: 'openlibrary', label: '2'},
      ]
    }
  }
  onSubmit () {

  }

  onChange (val) {
    console.log(val)
  }

  bibkeyOnChange(e) {

  }

  bibvalueOnChange(e) {

  }

  render () {
    return <div>
      <form onsubmit={this.onSubmit.bind(this)}>
        <Select
          options={this.state.identifers}
          value={this.state.selectedIdentifier}
          onChange={this.bibkeyOnChange.bind(this)} />
        <input
          type='text'
          name='bibvalue'
          value={this.state.bibvalue}
          onChange={this.bibvalueOnChange.bind(this)} />
        <button>Lookup</button> 
      </form>
    </div>
  }
}

LookupForm.propTypes = {
  identifers: React.PropTypes.array,
  selectedIdentifier: React.PropTypes.any,
  value: React.PropTypes.any,
}

ReactDOM.render(
  <LookupForm />,
  document.getElementById('lookup')    
);*/
