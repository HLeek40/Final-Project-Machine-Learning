function init(){
    var selector = d3.select("#selDataset");
    d3.json("/cat_list").then((sampleNames) => {
        sampleNames.forEach((sample) => {
          selector
            .append("option")
            .text(sample)
            .property("value", sample);
            //console.log(sample);
        });
    });
}
function displayReviews(pid){
    var selector = d3.select("#main-content");
    selector.html("");
    //console.log("got here reviews");
    //console.log(pid);
    d3.json(`/reviews/${pid}`).then(function(data){
        Object.entries(data).forEach((key) => {
            let rev = key[1];
            selector.append('card')
            .attr('class', 'card-body text-center')
            .append('p')
            .attr('class', 'card-text')
            .text(rev.text)
            .append('br')
            // one
            // .append('card-body')
            // .text(rev.text)
            // .append('br')
            // .append('br');
        })
    });
}
function displayProducts(cat){
    var selector = d3.select("#main-content");
    selector.html("");
    var labels = ['Positive','Negative','Neutral','Compound'];
    selector.append('div').attr('id', cat);
    var values = [];
    d3.json(`/cat_reviews/${cat}`).then(function(data){
        values.push(data.pos);
        values.push(data.neg);
        values.push(data.neu);
        values.push(data.com);
    });
    var trace = {
        x: labels,
        y: values,
        name: cat,
        type: 'bar'
    };
    var tData = [trace];
    var layout = {
        title: cat
    };
    var bub = document.getElementById(cat);
    Plotly.newPlot(bub, tData, layout);

    d3.json(`/products/${cat}`).then(function(c){
        Object.entries(c).forEach((key) => {
            let product = key[1];
            var one = selector.append('figure');
            let pid = product.product_id;
            one
            .append('img')
            .attr('src', product.link_image)
            .attr('height', 200)
            .attr('width', 200)
            .attr('align', 'left')
            .attr('alt', product.name)
            .attr('title', product.name)
            .on('click', function() { displayReviews(pid) });
        });
    });
}

function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    displayProducts(newSample);
  }
  
init();