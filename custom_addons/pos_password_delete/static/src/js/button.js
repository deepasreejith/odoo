/** @odoo-module */
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";

export class Button extends Component {

    static template = "pos_password_delete.Button";
     // Setup method
    setup() {
       this.popup = useService("popup");
       this.pos = usePos();
    }

    async click() {
        console.log("My Custom Button clicked!");
        const { confirmed, payload } = await this.popup.add(NumberPopup, {
            title: _t("Enter Password"),
            body: _t("Please enter the password to delete the item."),
            isPassword: true,
        });
        if (confirmed) {
            const password = payload;
            const correctPassword = this.pos.config.delete_order_password || '';
            if (password === correctPassword) {
                 const selectedOrder = this.pos.get_order();
                const selectedLine = selectedOrder.get_selected_orderline();
                if (selectedLine) {
                    selectedOrder.orderlines.remove(selectedLine);
                    console.log("Item deleted successfully.");
                } else {
                    console.log("No item selected.");
                }
            } else {
                 this.popup.add(ErrorPopup, {
                    title: _t("Invalid Password"),
                    body:_t("The password you entered is incorrect."),
                });
            }
        }
    }
}
ProductScreen.addControlButton({
    component: Button,
    condition: () => true,
});
