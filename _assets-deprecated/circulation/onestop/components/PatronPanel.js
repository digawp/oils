import React, { Component, PropTypes } from 'react'

class PatronLookupForm extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      patron: this.props.patron || '',
    };
  }

  handleChange(e) {
    this.setState({ patron: e.target.value });
  }

  handleSubmit(e) {
    const patron = e.target.value.trim();
    if (e.key === 'Enter' && patron !== '') {
      this.props.onLookup(patron);
    }
  }

  render() {
    return (
      <div>
        <label htmlFor="patron-lookup">Patron</label>
        <input
          type="text"
          id="patron-lookup"
          value={this.state.patron}
          onChange={this.handleChange.bind(this)}
          onKeyDown={this.handleSubmit.bind(this)} />
      </div>
    );
  }
}

PatronLookupForm.propTypes = {
  onLookup: PropTypes.func.isRequired,
  patron: PropTypes.string,
}


class PatronDetail extends Component {
  render() {
    const { patronProfile } = this.props;
    return (
      <div>
        ID: {patronProfile.id} <br />
        Name: {patronProfile.name} <br/>
        Email: {patronProfile.email} <br/>
        Loan Limit: {patronProfile.loan_limit} <br/>
      </div>
    );
  }
}

class PatronPanel extends Component {
  render(){
    const { patronProfile, onLookup } = this.props;
    return (
      <div>
        <PatronLookupForm
          patronId={patronProfile.id}
          onLookup={onLookup} />
        {
          patronProfile.id ? (
            <PatronDetail
              patronProfile={patronProfile} />
          ) : null
        }
      </div>
    );
  }
}

export default PatronPanel;
