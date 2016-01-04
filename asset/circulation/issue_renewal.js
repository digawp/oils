import 'react-select/less/default.less'
import React from 'react'
import ReactDOM from 'react-dom'

import ResourceMultiSelect from './components/ResourceMultiSelect';


ReactDOM.render(
        <div>
            <ResourceMultiSelect label="Resource ID" />
        </div>,
        document.getElementById('issue-form')
);
