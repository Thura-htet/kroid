(this["webpackJsonpkroid-web"]=this["webpackJsonpkroid-web"]||[]).push([[0],{10:function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a),c=n(3),r=n.n(c),i=(n(9),n(1));function l(e){var t=Object(a.useState)(null),n=Object(i.a)(t,2),c=n[0],r=n[1],l=Object(a.useState)(!1),s=Object(i.a)(l,2),m=s[0],d=s[1],p=Object(a.useState)([]),f=Object(i.a)(p,2),h=f[0],v=f[1];return Object(a.useEffect)((function(){fetch("http://localhost:8000/api/posts").then((function(e){return e.json()})).then((function(e){d(!0),v(e)}),(function(e){d(!0),r(e)}))}),[]),c?o.a.createElement("div",null,"Error: ",c.message):m?h.map((function(e,t){return o.a.createElement(u,{post:e,key:"".concat(t,"-{post.id}")})})):o.a.createElement("div",null,"Loading...")}function s(e){e.post;return"save"===e.action.type?o.a.createElement("button",null,"Save"):null}function u(e){var t=e.post,n=e.className?e.className:"col-10 mx-auto column-md-6";return o.a.createElement("div",{className:n},o.a.createElement("p",null,t.id," - ",t.title),o.a.createElement("div",null,o.a.createElement(s,{post:t,action:{type:"save"}})))}Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));r.a.render(o.a.createElement(l,null),document.getElementById("kroid")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))},4:function(e,t,n){e.exports=n(10)},9:function(e,t,n){}},[[4,1,2]]]);
//# sourceMappingURL=main.77a37c2f.chunk.js.map