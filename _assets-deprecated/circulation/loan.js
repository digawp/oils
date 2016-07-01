import 'react-select/less/default.less'
import React from 'react'
import ReactDOM from 'react-dom'

import ResourceMultiSelect from './components/ResourceMultiSelect';
import PatronSelect from './components/PatronSelect';


ReactDOM.render(
        <div>
            <PatronSelect />
            <ResourceMultiSelect label="Resource ID" />
        </div>,
        document.getElementById('loan-form')
);
