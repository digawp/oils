import React, { Component } from 'react'

class ItemInformation extends Component {
    render(){
        let { item } = this.props
        if (Object.keys(item).length === 0) return null
        if (item.detail === "Not found.") return (<div>Not Found</div>)

        return (
            <div>
              <dl>
                <dt>Item Code</dt>
                <dd>{ item.code }</dd>
                <dt>Book Classification</dt>
                <dd>{ item.classifications }</dd>
                <dt>Title</dt>
                <dd>{ item.title }</dd>
                <dd>{ item.subtitle }</dd>
                <dt>Authors</dt>
                <dd>{ item.authors }</dd>
              </dl>
            </div>
        )
    }
}

export { ItemInformation }
