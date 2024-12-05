/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

console.log(" JS file loaded..")
    publicWidget.registry.SnippetLatestProducts = publicWidget.Widget.extend({
        selector: '.three_product_dynamic_snippet',

        start: async function () {
            console.log("Widget is starting...");
            var self = this;
            var data = jsonrpc('/three_product_list', {}).then((data) => {
                console.log(data);
                self.$target.empty().append(data)
                console.log("test")
            });
        },
     });

export default publicWidget.registry.SnippetLatestProducts;
