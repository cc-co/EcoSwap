function show_new_product_list(products) {
    const product_list_element = document.getElementById('product_list');

    if (products.length == 0) {
        product_list_element.innerHTML = '<p>(No products found. Select an/another category)</p>'
    } else {
        let product_list_items = '';
        products.forEach(function(product) {
            product_list_items += '<li>' + product.name +` : `+ product.product_des + '</li>\n'
        })
        product_list_element.innerHTML = '<ul>\n' + product_list_items + '</ul>\n'
    }
}

// This function generates results in HTML FROM THE API, GET put/shows items into <ul><li><li></ul>

function update_product_list(category_id) {
    if (category_id < 0)
    {
        show_new_product_list([])
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "/api/product?category_id=" + category_id.toString());

        xhr.onload = function (evt) {
            if (this.status == 200) {
                var products = JSON.parse(this.responseText);
                show_new_product_list(products);
            } else {
                show_new_product_list([])
            }
        }

        xhr.send();
    }
}

//The read-only XMLHttpRequest property responseText returns the text received from a server following a request being sent.

window.onload = (event) => {
    const dropdown = document.getElementById('category_id');
    dropdown.onchange = function(){
        const category_id = dropdown.options[dropdown.selectedIndex].value;
        update_product_list(category_id);
    }
};

// making dropdown possible