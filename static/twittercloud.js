var myConfig = {
  type: 'wordcloud',
  options: {
    text: '',
  }
};

function get_keywords(){
  $.ajax({
      url: 'get_keywords',
      type: 'get',
      success:function(data){
          var keywords = JSON.parse(data);
          console.log(keywords);
          for(var i=0;i<keywords.length;i++){
            $("#keywords").append("<div class='keyword' data-keyword='" + keywords[i]._id + "' href='#'>" + keywords[i]._id + "(" + keywords[i].count + ")</div><br>");
          }
      }
  });
}


function create_cloud(data){
  zingchart.render({ 
    id: 'myChart', 
    data: data, 
    height: 400, 
    width: '100%' 
  });
}


$( document ).ready(function() {;
  console.log("ready")
  get_keywords();
});

$("#keywords").on('click',".keyword",function(){
  var keyword = $(this).data('keyword');
  $.ajax({
      url: 'get_words',
      type: 'post',
      data: {"keyword":keyword},
      success:function(data){
          console.log(data);
          myConfig.options.text = data;
          create_cloud(myConfig);
      }
  });
})