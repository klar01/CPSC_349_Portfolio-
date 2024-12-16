 
const overviewBtn = document.getElementById("overview");
const documentBtn = document.getElementById("docs");
const linkBtn = document.getElementById("links");

let overviewSection= document.getElementById("secttion-overview");
let docSection = document.getElementById("section-docs");
let linkSection = document.getElementById("section-links");

//to hide the other sections besides OVERVIEW
overviewBtn.addEventListener("click", function(){
    overviewSection.style.display = "inline";
    docSection.style.display = "none";
    linkSection.style.display = "none";  

})

//to hide the other sections besides DOCS
documentBtn.addEventListener("click", function(){
    overviewSection.style.display = "none";
    docSection.style.display = "inline";
    linkSection.style.display = "none";

})

//to hide the other sections besides LINKS
linkBtn.addEventListener("click", function(){
    overviewSection.style.display = "none";
    docSection.style.display = "none";
    linkSection.style.display = "inline";

})