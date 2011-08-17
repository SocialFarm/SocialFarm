//jquery.dform-0.1.3.min

(function(a){function h(b,c,e){if(typeof c=="string"){a.isArray(b[c])||(b[c]=[]);b[c].push(e)}else typeof c=="object"&&a.each(c,function(g,i){h(b,g,i)})}var f={},d={};a.fn.extend({runSubscription:function(b,c,e){var g=this;a.dform.hasSubscription(b)&&a.each(f[b],function(i,j){j.call(a(g),c,e)});return this},runAll:function(b){var c=b.type,e=this;this.runSubscription("[pre]",b,c);a.each(b,function(g,i){a(e).runSubscription(g,i,c)});this.runSubscription("[post]",b,c);return this},formElement:function(b,
c){if(c&&a.dform.converters&&a.dform.converters[c])b=a.dform.converters[c](b);var e=a.dform.createElement(b);this.append(a(e));a(e).runAll(b);return this},buildForm:function(b,c,e){if(typeof b=="string"){var g=a(this);a.get(b,c,function(i,j,k){a(g).buildForm(i);a.isFunction(e)&&e(i,j,k)},a.dform.options.ajaxFormat)}else{b.type||(b=a.extend({type:"form"},b));if(this.is(b.type)){this.dformAttr(b);this.runAll(b)}else this.formElement(b,c)}return this},dformAttr:function(b,c){var e=a.keyset(f);a.isArray(c)&&
a.merge(e,c);this.attr(a.withoutKeys(b,e));return this}});a.extend(a,{keyset:function(b){var c=[];a.each(b,function(e){c.push(e)});return c},withKeys:function(b,c){var e={};a.each(c,function(g,i){if(b[i])e[i]=b[i]});return e},withoutKeys:function(b,c){var e={};a.each(b,function(g,i){if(a.inArray(g,c)==-1)e[g]=i});return e},getValueAt:function(b,c){for(var e=a.isArray(c)?c:c.split("."),g=b,i=0;i<e.length;i++){var j=e[i];if(!g[j])return false;g=g[j]}return g}});a.dform={options:{prefix:"ui-dform-",
ajaxFormat:"json",defaultType:function(b){return a("<"+b.type+">").dformAttr(b)}},removeType:function(b){delete d[b]},typeNames:function(){return a.keyset(d)},addType:function(b,c){h(d,b,c)},addTypeIf:function(b,c,e){b&&a.dform.addType(c,e)},subscriberNames:function(){return a.keyset(f)},subscribe:function(b,c){h(f,b,c)},subscribeIf:function(b,c,e){b&&a.dform.subscribe(c,e)},removeSubscription:function(b){delete f[b]},hasSubscription:function(b){return f[b]?true:false},createElement:function(b){var c=
b.type;if(!c)throw"No element type given! Must always exist.";var e=null;if(d[c]){var g=a.withoutKeys(b,"type");a.each(d[c],function(i,j){e=j.call(e,g)})}else e=a.dform.options.defaultType(b);return a(e)}}})(jQuery);
(function(a){a.fn.placeholder=function(h){if(a(this).val()==""){var f=this;a(this).data("placeholder",h);a(this).val(h);a(this).focus(function(){a(this).val()==a(this).data("placeholder")&&a(this).val("")});a(this).blur(function(){a(this).val()==""&&a(this).val(a(this).data("placeholder"))});h=a(this).parents("form");h.submit(function(){a(f).val()==a(f).data("placeholder")&&a(f).val("")});a('input[type="reset"]',h).click(function(){a(f).val(a(f).data("placeholder"))})}return this}})(jQuery);
(function(a){function h(f,d){return function(b){return a(f).dformAttr(b,d)}}a.dform.addType({container:h("<div>"),form:h("<form>"),text:h('<input type="text" />'),password:h('<input type="password" />'),submit:h('<input type="submit" />'),reset:h('<input type="reset" />'),hidden:h('<input type="hidden" />'),radio:h('<input type="radio" />'),checkbox:h('<input type="checkbox" />'),checkboxes:h("<div>",["name"]),radiobuttons:h("<div>",["name"]),file:h('<input type="file" />')});a.dform.subscribe({"class":function(f){this.addClass(f)},
html:function(f){this.html(f)},elements:function(f){var d=a(this);a.each(f,function(b,c){if(typeof b=="string")c.name=name;a(d).formElement(c)})},value:function(f){this.val(f)},options:function(f,d){var b=a(this);if(d=="select")a.each(f,function(c,e){var g={type:"option"};if(typeof e=="string"){g.value=c;g.html=e}if(typeof e=="object")g=a.extend(g,e);a(b).formElement(g)});else if(d=="checkboxes"||d=="radiobuttons"){b=this;a.each(f,function(c,e){var g=d=="radiobuttons"?{type:"radio"}:{type:"checkbox"};
if(typeof e=="string")g.caption=e;else a.extend(g,e);g.value=c;a(b).formElement(g)})}},caption:function(f,d){var b={};if(typeof f=="string")b.html=f;else a.extend(b,f);if(d=="fieldset"){b.type="legend";var c=a.dform.createElement(b);this.prepend(c);a(c).runAll(b)}else{b.type="label";if(this.attr("id"))b["for"]=this.attr("id");c=a.dform.createElement(b);d=="checkbox"||d=="radio"?this.parent().append(a(c)):a(c).insertBefore(a(this));a(c).runAll(b)}},type:function(f,d){a.dform.options.prefix&&this.addClass(a.dform.options.prefix+
d)},"[post]":function(f,d){if(d=="checkboxes"||d=="radiobuttons")this.children("[type="+(d=="checkboxes"?"checkbox":"radio")+"]").each(function(){a(this).attr("name",f.name)})}})})(jQuery);
(function(a){function h(d,b){var c=a.keyset(a.ui[d].prototype.options);return a.withKeys(b,c)}function f(d){d=d.split(".");if(d.length>1){var b=d.shift();if(b=jQuery.global.localize(b))return a.getValueAt(b,d)}return false}a.dform.subscribeIf(a.isFunction(a.fn.placeholder),"placeholder",function(d,b){if(b=="text"||b=="textarea")a(this).placeholder(d)});a.dform.addTypeIf(a.isFunction(a.fn.progressbar),"progressbar",function(d){return a("<div>").dformAttr(d).progressbar(h("progressbar",d))});a.dform.addTypeIf(a.isFunction(a.fn.slider),
"slider",function(d){return a("<div>").dformAttr(d).slider(h("slider",d))});a.dform.addTypeIf(a.isFunction(a.fn.accordion),"accordion",function(d){return a("<div>").dformAttr(d)});a.dform.addTypeIf(a.isFunction(a.fn.tabs),"tabs",function(d){return a("<div>").dformAttr(d)});a.dform.subscribeIf(a.isFunction(a.fn.accordion),"entries",function(d,b){var c=this;b=="accordion"&&a.each(d,function(e,g){a.extend(g,{type:"container"});a(c).formElement(g);a(c).children("div:last").prev().wrapInner(a("<a>").attr("href",
"#"))})});a.dform.subscribeIf(a.isFunction(a.fn.tabs),"entries",function(d,b){var c=this;if(b=="tabs"){this.append("<ul>");var e=a(c).children("ul:first");a.each(d,function(g,i){var j=i.id?i.id:g;a.extend(i,{type:"container",id:j});a(c).formElement(i);var k=a(c).children("div:last").prev();a(k).wrapInner(a("<a>").attr("href","#"+j));a(e).append(a("<li>").wrapInner(k))})}});a.dform.subscribeIf(a.isFunction(a.fn.dialog),"dialog",function(d,b){if(b=="form"||b=="fieldset")this.dialog(d)});a.dform.subscribeIf(a.isFunction(a.fn.resizable),
"resizable",function(d){this.resizable(d)});a.dform.subscribeIf(a.isFunction(a.fn.datepicker),"datepicker",function(d,b){b=="text"&&this.datepicker(d)});a.dform.subscribeIf(a.isFunction(a.fn.autocomplete),"autocomplete",function(d,b){b=="text"&&this.autocomplete(d)});a.dform.subscribe("[post]",function(d,b){if(this.parents("form").hasClass("ui-widget")){if((b=="button"||b=="submit")&&a.isFunction(a.fn.button))this.button();a.inArray(b,["text","textarea","password","fieldset"])!=-1&&this.addClass("ui-widget-content ui-corner-all")}if(b==
"accordion"){var c=h(b,d);a.extend(c,{header:"label"});this.accordion(c)}else if(b=="tabs"){c=h(b,d);this.tabs(c)}});a.dform.subscribeIf(a.isFunction(a.fn.validate),{"[pre]":function(d,b){if(b=="form"){var c={};if(this.hasClass("ui-widget"))c={highlight:function(e){a(e).addClass("ui-state-highlight")},unhighlight:function(e){a(e).removeClass("ui-state-highlight")}};this.validate(c)}},validate:function(d){this.rules("add",d)}});a.dform.subscribeIf(a.isFunction(a.fn.ajaxForm),"ajax",function(d,b){b==
"form"&&this.ajaxForm(d)});a.dform.subscribeIf(a.global&&a.isFunction(a.global.localize),"html",function(d){(d=f(d))&&a(this).html(d)});a.dform.subscribeIf(a.global,"options",function(d,b){if(b=="select"&&typeof d=="string"){a(this).html("");var c=f(d);c&&a(this).runSubscription("options",c,b)}});a.dform.subscribeIf(a.isFunction(a.fn.wysiwyg),"wysiwyg",function(){})})(jQuery);