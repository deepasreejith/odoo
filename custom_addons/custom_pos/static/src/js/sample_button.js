/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { SamplePopupButton } from "@custom_pos/js/sample_popup_button";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";

export class SampleButton extends Component {

    static template = "custom_pos.SampleButton";

    // Setup method
    setup() {
       this.pos = usePos();
       this.popup = useService("popup");
    }
    getSelectedOrderline(){
        const order = this.pos.get_order();
        console.log(order);
        return order ? order.get_selected_orderline() : null;
    }
    // Method to handle button click
    async click() {
        console.log("My Custom Button clicked!");
        const selectedOrder = this.getSelectedOrderline();
        if (selectedOrder) {
            const { confirmed, value } = await this.popup.add(SamplePopupButton);
            if (confirmed && value) {
                this.changeQuantity(value);
            }
        } else {
            console.log("No product selected!");
        }
    }

    changeQuantity(value) {
        const selectedOrder = this.getSelectedOrderline();
        if (selectedOrder && value > 0) {
            selectedOrder.set_quantity(parseInt(value));
            console.log(`Quantity changed to ${value}`);
        }
    }
}
ProductScreen.addControlButton({
    component: SampleButton,
    condition: () => true,
});

