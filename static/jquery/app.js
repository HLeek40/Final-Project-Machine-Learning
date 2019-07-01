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
function reviewPieChart(data){
    console.log(data);
    var newWin = window.open("","","width=500,height=500,scrollbars=1,resizeable=1");
    var labels = ['Positive','Negative','Neutral'];
    var html = "<html><head><script src=\"https://cdn.plot.ly/plotly-1.31.2.min.js\"></script></head><body></body></html>";
    newWin.document.write(html);
    var dat = [{
        values: data,
        labels: labels,
        type: 'pie'
    }];

    var layout = {
        height: 400,
        width: 400,
        title: 'Review Breakdown'
    };
    Plotly.newPlot(newWin.document.body,dat,layout);
}
function displayReviews(pid){
    var selector = d3.select("#main-content");
    selector.html("");
    d3.json(`/reviews/${pid}`).then(function(data){
        Object.entries(data).forEach((key) => {
            let rev = key[1];
            var pos = rev.vPositive * 100;
            var neg = rev.vNegative * 100;
            var neu = rev.vNeutral * 100;
            var analysis_array = [pos,neg,neu];
            var result_str = "";
            var r2_str = result_str.concat('Positive: ',pos,'%',' Negative: ',neg,'%',' Neutral: ',neu,'%');
            console.log(r2_str);
            var one = selector.append('div').attr('class', 'card').attr('style', 'width: 60rem');
            one
            .append('div')
            .attr('class', 'card-body')
            .append('p')
            .attr('class', 'card-text')
            .text(rev.input_time)
            .append('p')
            .attr('class', 'card-text')
            .text(rev.text)
            .append('p')
            .attr('class', 'card-text')
            .text('Review analysis')
            .append('p')
            .attr('class', 'card-text')
            .text(r2_str)
            .on('click', function() { reviewPieChart(analysis_array) });
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