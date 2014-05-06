//jq('#bcode-img').pin();
//jq('.pin-wrapper').removeClass('style');
//jq('.pin-wrapper').css({'height':'0'});
jq('#article-dialog').on('show.bs.modal', function (e) {
	
	var url = '../get_article_by_id/' + jq(e.relatedTarget).attr('article-id');
    
	jq.getJSON(url,function(article){
        	jq('#article-title').html(article.title);
        	jq('#publish-date').html(article.publish_date);
        	jq('#article-content').html(article.content);
    });
	
});

setInterval('get_user_count();',3000);

function get_user_count(){
	
	var url = '../get_user_count/'
	
	jq.ajax({
	    url:url,
 	    success:function(data){
 	    	var val = jq("#count").text();
 	    	if (data != val ){
 	    		jq("#count").text(data);
 	    		//jq('#count').css({'color':'#6699CC','font-size':'100px'});
 	    		//setTimeout("jq('#count').css({'color':'#bbb','font-size':'50px'})",1000);
 	    		if (data < val){
 	    			jq('#count').css({'color':'#CC6666'});
 	    			jq('#count').animate({fontSize:'10px'},300);
 	    			jq('#count').animate({fontSize:'60px'},300);
 	    			//jq('#count').css({'color':'#bbb'});
 	    		}else{
 	    			jq('#count').css({'color':'#6699CC'});
 	    			jq('#count').animate({fontSize:'100px'},300);
 	    			jq('#count').animate({fontSize:'60px'},300);
 	    			//jq('#count').css({'color':'#bbb'});
 	    		}
 	    	}
	    },

	});
}

/*var SpeechRecognition = window.SpeechRecognition || 
    window.webkitSpeechRecognition || 
    window.mozSpeechRecognition || 
    window.oSpeechRecognition || 
    window.msSpeechRecognition;

if (SpeechRecognition) {    
	  
	}*/

jq(function () {
	
	var url = '../get_article_by_offset/1';
    
	jq.getJSON(url,function(article_list){
		
    var page_count = Math.ceil(article_list.article_count / 10);
    generate_paging(page_count);

    jq("#article-pagination a").click(function(e){
        get_article_by_offset(jq(e.target).text());
    });
    
    });
	
});

function get_article_by_offset(offset){
	
	var url = '../get_article_by_offset/' + offset;
	    
	jq.getJSON(url,function(article_list){
		
    var articles = article_list.article_list;
    jq("#article-list").empty();
    for(i in articles){
        var j = parseInt(i) + 1;
        html_li = '<li>';
        html_li += '<span class="label label-default order-label">' + j + '</span>';
        if(offset==1 && j==1){
            html_li += '<a article-id="' + articles[i]['id'] + '" href="#article-dialog" class="navbar-link"  data-toggle="modal">' + articles[i]['title'] + '<span class="badge badge-new">new</span></a>';
        }else{
            html_li += '<a article-id="' + articles[i]['id'] + '" href="#article-dialog" class="navbar-link"  data-toggle="modal">' + articles[i]['title'] + '</a>';
        }
        html_li += '<span class="label label-default date-label">' + articles[i]['publish_date'] + '</span>';
        html_li += '</li>';
        jq("#article-list").append(html_li);
    }
    });
}

function generate_paging(page_count){

	if(page_count > 1){
		paging_html = '<ul class="pagination pagination-sm" id="article-pagination">';
		paging_html += '<li><a href="javascript:void(0);"><i class="icon-backward"></i></a></li>';
		
		for(i=1;i<=page_count;i++){
			paging_html += '<li><a href="javascript:void(0);">' + i + '</a></li>';
		}
		
		paging_html += '<li><a href="javascript:void(0);"><i class="icon-forward"></i></a></li>';
		paging_html += '</ul>';
		
		jq("#article-news").append(paging_html);
	}

}