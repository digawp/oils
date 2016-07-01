import React, { Component } from 'react'
import Select from 'react-select'

class TypedInput extends Component {
  render() {
    const { key, value } = this.props

    return <div>
      <input className='textbox' name='identifier-value' type='text'
        value={this.value} />
      <button className='action'>Go</button>
    </div>
  }
}

class ExpandableTypedInput extends Component {
  render() {

    return <div className='expandable-input'>
      <ul>
        <TypedInput />
      </ul>
    </div>
  }
}

class TitleInput extends Component {
  handleChange(e){
    console.log(e);
  }
  render() {
    const { title } = this.props;
    return <div>
      <label>Title</label>
      <input type='text' value={title} onChange={this.handleChange.bind(this)}/>
    </div>
  }
}
class SubtitleInput extends Component {
  handleChange(e){
    console.log(e);
  }
  render() {
    const { subtitle } = this.props;
    return <div>
      <label>Subtitle</label>
      <input type='text' value={subtitle} onChange={this.handleChange.bind(this)}/>
    </div>
  }
}

class AnnotationPanel extends Component {
  render() {
    return <div>
      Form
    </div>
  }
}

class HoldingPanel extends Component {
  render() {
    return <div>
      Form
    </div>
  }
}

const ClassificationInput = () => (
  <div>
    <label>Classification</label>
  </div>
)

const AuthorInput = ()=>(
  <div>
    <label>Author</label>
    <Select multi={true} />
  </div>
)

const PublisherInput = ()=>(
  <div>
    <label>Publisher</label>
    <Select multiple={true} />
  </div>
)

const PublicationYearInput = ({year})=>(
  <div>
    <label>Publiction Year</label>
    <input type='text' value={year} />
  </div>
)

class BibliographicPanel extends Component {
  render() {
    const { bibliographic } = this.props;

    return <div>
      <TitleInput title={bibliographic.title} />
      <SubtitleInput subtitle={bibliographic.subtitle} />
      <ClassificationInput classifications={bibliographic.classifications} />
      <AuthorInput authors={bibliographic.authors} />
      <PublisherInput publishers={bibliographic.publishers} />
      <PublicationYearInput year='' />
    </div>
  }
}

class ActionPanel extends Component {
  handleCancel(e){

  }
  handleSaveContinue(e){

  }
  handleSaveClose(e){

  }
  render() {
    return <div>
      <button type='button'
        onClick={this.handleCancel.bind(this)}>Cancel</button>
      <button type='button' onClick={this.handleSaveContinue.bind(this)}>
        Save
      </button>
      <button type='button' onClick={this.handleSaveClose.bind(this)}>
        Save & Close
      </button>
    </div>
  }
}

class CatalogForm extends Component {
  render() {
    const { item } = this.props;
    return <div>
      <BibliographicPanel bibliographic={item.bibliographic} />
      <AnnotationPanel annotations={item.annotations}/>
      <HoldingPanel holdings={item.holdings}/>
      <ActionPanel />
    </div>
  }
}


export default CatalogForm;
