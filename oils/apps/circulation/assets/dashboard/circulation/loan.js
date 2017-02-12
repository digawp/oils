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
})

var Patron = Backbone.Model.extend({
  defaults: {
    username: '',
    name: '',
    address: '',
  },    
  urlRoot: '/api/accounts/patrons',
})
let patron = new Patron()


var PatronInfoView = Backbone.View.extend({
  template: _.template(_.unescape($('#patron-info-template').html())),
  initialize(options){
    this.patron = options.patron
  },
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
    this.delayedUpdatePatron = _.debounce(this.updatePatron.bind(this), 1000),
    this.patronInfoView = new PatronInfoView({el: $('.patron-info')})
    let initialVal = this.$el.find('input').val()
    this.delayedUpdatePatron(initialVal)
  },
  updatePatron(username){
    if (username){
      patron = new Patron({id: username});
      patron.on('change', ()=>{
        this.patronInfoView.patron = patron
        this.patronInfoView.render()
      }, this)
      patron.fetch()
    }
  },
  patronChanged(e){
    this.delayedUpdatePatron($(e.currentTarget).val())
  },
})


var patronView = new PatronView({el: $('#div_id_patron')})

$('div[id^=div_id_loan_set]').each(function(index){
  new ItemView({index, el: $(this)})
})
