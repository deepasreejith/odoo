/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useRef } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class PopupButton extends AbstractAwaitablePopup {

    static template = "pos_popup.PopupButton";

    setup() {
       super.setup();
       this.inputRef = useRef("inputRef");
       this.pos = usePos();
    }
    static defaultProps = {
        closePopup: _t("Cancel"),
        confirmText: _t("OK"),
        title: 'Enter Barcode',
    };

     confirm() {
        const barcodeValue = this.inputRef.el.value;
        if (barcodeValue) {
            this.removeBarcodeProducts(barcodeValue);
            this.props.close();
        } else {
            console.warn("No barcode entered.");
        }
    }

    removeBarcodeProducts(barcode) {
        const order = this.pos.get_order();
        const orderLines = order.get_orderlines();
        if (orderLines.length>0){
            const linesToRemove = orderLines.filter(line => line.product.barcode === barcode);
            console.log(linesToRemove)
            if (linesToRemove.length > 0) {
                linesToRemove.forEach(line => {
                    order.orderlines.remove(line);
                });
                console.log(`products with barcode ${barcode} removed.`);
            } else {
                console.warn(`No products found with barcode ${barcode}.`);
            }
        } else {
            console.error("No Products in order found.");
        }
    }
}