import Backbone from 'backbone'
import _ from 'underscore'
import $ from 'jquery'

var Item = Backbone.Model.extend({
  defaults: {
    code: '',
    title: '',
    identifiers: {},
  },
  urlRoot: '/api/shelving/items',
})

var ItemInfoView = Backbone.View.extend({
  template: _.template(_.unescape($('#item-info-template').html())),
  initialize(options){
    this.item = options.item
  },
  render(){
    let data = {item: this.item.toJSON()}
    this.$el.html(this.template(data))
    return this
  }
})

let ItemView = Backbone.View.extend({
  events: {
    'input input': 'itemChanged',
  },
  initialize(options){
    this.delayedUpdateItem = _.debounce(this.updateItem.bind(this), 1000)
    this.itemInfoView = new ItemInfoView({el: $(`.items-info-${options.index}`)})
    let initialVal = this.$el.find('input').val()
    this.delayedUpdateItem(initialVal)
  },
  updateItem(item_code){
    this.item = new Item({id: item_code})
    if (!item_code) {
      this.itemInfoView.$el.empty()
      return
    }
    this.item.on('change', ()=>{
      this.itemInfoView.item = this.item
      this.itemInfoView.render()      
    }, this)
    this.item.fetch()
  },
  itemChanged(e){
    let item_code = $(e.currentTarget).val()
    this.delayedUpdateItem(item_code)
  },
  template: _.template(_.unescape($('#item-info-template').html())),
  render(){
    this.$el.append(this.itemInfoView.$el)
    this.itemInfoView.render()
    return this
  }
})

var Patron = Backbone.Model.extend({
  defaults: {
    username: '',
    name: '',
    address: '',
  },    
  urlRoot: '/api/accounts/patrons',
  initialize(){
    this.on('change', (model, resp)=>{
      patronView.render()                                    
    })
  },
})
let patron = new Patron()


var PatronInfoView = Backbone.View.extend({
  template: _.template(_.unescape($('#patron-info-template').html())),
  render(){
    let data = {patron: patron.toJSON()}
    this.$el.html(this.template(data))
    return this
  }
})


var PatronView = Backbone.View.extend({
  events: {
    'input input#id_patron': 'patronChanged',
  },
  initialize() {
    this.patronInfoView = new PatronInfoView()
    let initialVal = this.$el.find('input').val()
    this.delayedPatronApi(initialVal)
  },
  delayedPatronApi: _.debounce((username)=>{
    if (username){
      patron = new Patron({id: username});
      patron.fetch()
    }
  }, 1000),
  patronChanged(e){
    this.delayedPatronApi($(e.currentTarget).val())
  },
  render(){
    this.$el.append(this.patronInfoView.$el)
    this.patronInfoView.render()
    return this
  }
})


var patronView = new PatronView({el: $('#patron-field')})

$('div[id^=div_id_loan_set]').each(function(index){
  console.log(index)
  new ItemView({index, el: $(this)})
})
