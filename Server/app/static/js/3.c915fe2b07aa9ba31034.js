webpackJsonp([3],{"6Sd8":function(t,e){},bqQt:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=function(){return n.e(8).then(n.bind(null,"2qqO"))},o=function(){return n.e(9).then(n.bind(null,"wtSN"))},r={name:"SurveyQuestion",props:{question:{type:Object}},computed:{component:function(){return this.question.is_objective?i:o}}},u={render:function(){var t=this,e=t.$createElement;return(t._self._c||e)(t.component,{tag:"div",staticClass:"question-wrapper",attrs:{question:t.question},on:{"update:question":function(e){return t.$emit("update:question",e)}}})},staticRenderFns:[]};var s={name:"SurveyDetailRight",components:{SurveyQuestion:n("VU/8")(r,u,!1,function(t){n("6Sd8")},"data-v-39ec851e",null).exports},data:function(){return{questions:[]}},props:{},methods:{load:function(){var t=this;this.$http.get("/survey/question",{headers:{Authorization:"JWT "+this.$cookie.getCookie("JWT")},params:{survey_id:this.$route.params.id}}).then(function(e){200===e.status?t.questions=e.data:204===e.status&&alert("존재하지 않는 설문조사입니다.")}).catch(function(t){console.log(t)})},submit:function(){var t=this,e=[];this.questions.forEach(function(n){var i=new FormData;i.append("question_id",n.id),i.append("answer",n.answer);var o=t.$http.post("/survey/question",i,{headers:{Authorization:"JWT "+t.$cookie.getCookie("JWT")}});e.push(o)}),this.$http.all(e).then(function(t){var e=t.filter(function(t){return 201===t.status});t.length===e.length?alert("설문조사 제출에 성공하였습니다."):alert("설문조사 제출에 실패하였습니다.")}).catch(function(){alert("설문조사 제출에 실패하였습니다.")})}},beforeMount:function(){this.load()}},a={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"survey-detail-right-wrapper"}},[n("div",{attrs:{id:"survey-form-wrapper"}},[t._l(t.questions,function(t){return n("survey-question",{key:t.id,attrs:{question:t},on:{"update:question":function(e){t=e}}})}),t._v(" "),n("div",{attrs:{id:"airplane-button"},on:{click:t.submit}})],2)])},staticRenderFns:[]};var c=n("VU/8")(s,a,!1,function(t){n("vd68")},"data-v-287aec86",null);e.default=c.exports},vd68:function(t,e){}});
//# sourceMappingURL=3.c915fe2b07aa9ba31034.js.map