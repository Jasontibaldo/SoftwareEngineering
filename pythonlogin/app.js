function myFunc() {
    var listSize = {{owner|tojson}};
    var jsonStr = JSON.stringify(listSize);
    document.write(jsonStr);
}