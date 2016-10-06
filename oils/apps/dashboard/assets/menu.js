import React, { Component } from 'react'
import ReactDOM from 'react-dom'

class MenuItem extends Component {
  constructor(props){
    super(props);
    let path = window.location.pathname;
    let reg = new RegExp('^' + props.url + '$');
    console.log(props.label);
    console.log(path)
    console.log(reg)
    console.log(reg.test(path));
    if (reg.test(path)){
      this.state = {
        showMenu: true
      };
      //props.onActiveChild()
    } else if (props.submenu.length > 0){
      this.state = {
        showMenu: false
      };
    }
  }

  activateParent(){
    this.setState({showMenu: true});
  }

  expandChild(e){
    if (this.props.submenu.length == 0){
      return;
    }

    this.setState({showMenu: !this.state.showMenu});
    e.preventDefault();
  }

  render(){
    let dropdownIcon = "";
    let submenu = "";
    let p = this;
    if (this.props.submenu.length >= 1 ){
      dropdownIcon = "fa fa-caret-down";
      if (this.state.showMenu){
        submenu = (
            <ul className='nav-list'>
            {this.props.submenu.map(function(m, i){
              return (
                <MenuItem
                  onActiveChild={p.activateParent.bind(this)}
                  key={i}
                  url={m.url}
                  label={m.label}
                  icon={m.icon}
                  submenu={m.children} />
              )
            })}
            </ul>
        );
      }
    }

    return (
        <li>
          <a href={this.props.url||'#'} onClick={this.expandChild.bind(this)}>
            <i className={this.props.icon + " menu-left-icon"}></i>
            {this.props.label}
            <i className={ dropdownIcon + " menu-right-icon"}></i>
          </a>
          { submenu }
        </li>
    );
  }
}

class Menu extends Component {
  render() {
    let menuItems = this.props.data['dashboard']['menu'].map(function(menuItem, i){
      return (
          <MenuItem
            key={i}
            url={menuItem.url}
            label={menuItem.label}
            icon={menuItem.icon}
            submenu={menuItem.children} />
      )
    });
    return (
      <div>
        <ul className="nav-list">
          { menuItems }
        </ul>
      </div>
    )
  }
}

document.addEventListener("DOMContentLoaded", function(event) {
    ReactDOM.render(
        <Menu data={window.initialData} />,
        document.getElementById('sidebar')
    );
});
