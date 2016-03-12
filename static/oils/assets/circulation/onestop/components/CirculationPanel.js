import React, { Component, PropTypes } from 'react'

class LoanActions extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      value: ''
    };
  }

  handleChange(e) {
    this.setState({value: e.target.value });
    this.props.onSelect(this.props.loan, this.state.value);
    this.setState({value: ''});
  }

  render() {
    return (
      <select onChange={this.handleChange.bind(this)} value={this.state.value}>
        <option value='' disabled>--Actions--</option>
        <option value='renew'>Renew</option>
        <option value='return'>Return</option>
        <option value='lost'>Lost</option>
      </select>
    );
  }
}

class LoanRow extends Component {
  render(){
    const { num, loan, actions } = this.props;
    return (
      <tr>
        <td><input type='checkbox' /></td>
        <td>{ num }</td>
        <td>{loan.resource.code}</td>
        <td>{loan.resource.title}</td>
        <td>{loan.loan_at}</td>
        <td><LoanActions loan={loan.id} onSelect={actions.selectLoanAction}/></td>
      </tr>
    );
  }
}

class LoanTable extends Component {
  render(){
    const { loans, actions } = this.props;

    return (
      <table>
        <thead>
          <tr>
            <th><input type='checkbox' /></th>
            <th>#</th>
            <th>Identifier</th>
            <th>Title</th>
            <th>Due Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {
            loans.map((obj, i) => {
              return (
                <LoanRow key={i} loan={obj} num={i+1} actions={actions}/>
              );
            })
          }
        </tbody>
      </table>
    );
  }
}



class CheckoutForm extends Component {

  constructor(props, context) {
    super(props, context);
    this.state = {
      resource: '',
    };
  }

  handleSubmit(e){
    e.preventDefault();
    this.props.onCheckout(this.props.patron, this.state.resource);
    this.setState({ resource : '' });
  }

  handleChange(e) {
    this.setState({
      resource: e.target.value,
    });
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit.bind(this)}>
          <label htmlFor="checkout-input">Resource Code:</label>
          <input
            type="text"
            id="checkout-input"
            value={this.state.resource}
            onChange={this.handleChange.bind(this)} />
          <button>Checkout</button>
        </form>
      </div>
    );
  }
}

class CirculationPanel extends Component {
  render(){
    const { patron, loans, actions } = this.props;
    return (
      <div>
        <CheckoutForm patron={patron} onCheckout={actions.checkoutResource} />
        <LoanTable loans={loans} actions={actions}></LoanTable>
      </div>
    );
  }
}

export default CirculationPanel;
