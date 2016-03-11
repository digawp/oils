import React, { Component, PropTypes } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import PatronPanel from '../components/PatronPanel'
import CirculationPanel from '../components/CirculationPanel'
import * as OneStopActions from '../actions'

// Containers App
class App extends Component {
  render(){
    const { patron, actions } = this.props;

    return (
      <div>
        <PatronPanel
          patronProfile={patron.profile}
          onLookup={actions.lookupPatron} /> 
        {
          patron.profile.id ? (
          <CirculationPanel
            patron={patron.profile.id}
            circulation={patron.circulation}
            actions={actions} />
            ) : null
        }
      </div>
    );
  }
}

App.propTypes = {
  patron: PropTypes.object.isRequired,
  actions: PropTypes.object.isRequired,
}

function mapStateToProps(state) {
  return {
    patron: state.patron,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(OneStopActions, dispatch)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App);
