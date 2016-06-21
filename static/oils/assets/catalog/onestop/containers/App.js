import React, { Component, PropTypes } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as OneStopActions from '../actions'





import CatalogForm from '../components/CatalogForm'

class App extends Component {
  render() {
    const { item, actions } = this.props;
    return <div>
      <CatalogForm item={item} />
    </div>
  }
}

App.propTypes = {
  item: PropTypes.object.isRequired,
  actions: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  console.log(state);
  return {
    item: state.item,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(OneStopActions, dispatch),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
