function gnbSearchPerfume(){
    const search_keyword = document.getElementById("gnb_searchinput").value;
    const search_url = "https://www.mmop-perfume.com/search.html?search="+search_keyword;
    location.href = search_url;
}

document.getElementById("gnb_searchinput").addEventListener("keypress", function(event){
    if(event.keyCode == 13){
        gnbSearchPerfume();
    }
});