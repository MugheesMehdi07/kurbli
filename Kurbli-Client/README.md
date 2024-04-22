## Installation and Integration

**Step 1: Download Library**

Download the library.Once the Library is downloaded, it is ready to be included in our applications.

**Step 2: BatchData Client Token Generation**

In order to create the client token get an account on https://batchdata.com/

**Step 3: Library Initialization**

To begin using our downloaded library in our applications, we  must first import our authentication details, preferably as environment variables.

Create a JavaScript file and include your Domain URL or IP Address, and Client Token.

```jsx
var env = {
    domainServer: 'myapp.mycompany.com',
    token: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
}
```

Next import the JavaScript Library, Styling Sheet Library and Environment Variables into your webapp with the following code.


```html
<link rel="stylesheet" href="<path to the downloaded library folder>/dist/batch-address-auto-complete.min.css">
<script src="<path to the downloaded library folder>/dist/batch-address-auto-complete.min.js"></script>
<script src="<path to the file>/environment.js"></script>
```

Next create a script initializing the library in the head tag

```jsx
<script>
function initialize() {
      // Custom Autocomplete of Batch Service
      batchAutocomplete(document.getElementById("batchAddressAutoComplete"), env.domainServer, env.token);

      // Add an event listener to get value
      document.addEventListener("batch-address-auto-complete", function(e) {
         // Here you will get data what you had selected in input by using "e.detail"
         console.log('Selected item: ', e.detail);
      });

      // Add an event listener to handle error
      document.addEventListener("batch-auto-complete-error", function (e) {
         // Here you will get error using "e.detail"
         console.log("Error while searching: ", e.detail);
      });
  }
  </script>
```

The above code first creates an instance of Batch Address Autocomplete library, then an event listener is added to capture keystrokes and begin making address suggestions leveraging the library.Once user selects the address, the selected input will be cought in event lister as e.detail. The address object will be as follows - 

```jsx
{
  address: "8568 hollyoak st"
  city: "buena park"
  linkedEntityId: "afpYNEIoHpm43Kw"
  name: "8568 Hollyoak St, Buena Park, CA 90620"
  state: "ca"
  type: "address"
  zip: "90620"
  _id: "31c49612b2452fa2644649cbf879f794"
}
```

 Finally another event handler is added to handle errors. If there is any error, the details will be catched by error event handler and can be accessed as e.detail. The object will be as follows -

```jsx
{
    "status": {
        "code": 404,
        "text": "Not Found",
        "message": "URL not found."
    }
}
```
**Step 4: UI Intergation**

Include following code inside your form or body tag to instanciate the library and to add input element on the page.


```html
<body onload="initialize()">
  ...
    <div class="batch-loading">
      <input class="batch-autocomplete" id="batchAddressAutoComplete" notFoundText="No results found" showNotFound=true
         displayData="name" type="text" take='5' debounce='700' placeholder="Enter your address">
      <div id="batch-loader"></div>
      <div id="batchNoDataFound"></div>
    </div>
  ...
</body>
```

**Step 5: Configuration**

Initailly library will be configured with deafult configurations. You can update these parameters as requried

`showNotFound`: This option is used to enable a text message for users when no results are found for the given string. By default it will be set as `true`. It can accept only boolen values.

`notFoundText`: This option is used to set the text to be shown when there are no results for the given input. By default it will set as `No results found`

`displayData`: This option is used to populate the data in the input box when user selects a record from searched result. By default it will populate `name` parameter returned for selected item. You can set it to populate - `state`, `address` , `name` , `zip` , `city`.

`take`: This option is used to set the number of searched results to be displayed when input is typed. By default it is set to `5`.

`debounce` : This option is used to delay the search API call when user is typing the keyword in input box. For example, If the value is set to `700`, the search API will get triggered after 700ms post last key stroke made within 700ms.
By default this value is set to `700`, It is recommended to keep this value to its default value to save the API calls.

Well done!! You can begin using Batch Address Autocomplete JavaScript Library in your application.