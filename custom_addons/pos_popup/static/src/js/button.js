/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { PopupButton } from "@pos_popup/js/popup_button";

export class Button extends Component {

     static template = "pos_popup.Button";
     // Setup method
    setup() {
       this.popup = useService("popup");
    }

    async click() {
        console.log("My Custom Button clicked!");
        await this.popup.add(PopupButton);
    }

}
ProductScreen.addControlButton({
    component: Button,
    condition: () => true,
});