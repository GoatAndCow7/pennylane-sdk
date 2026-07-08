# Facturation électronique française (réforme 2026)

La France rend obligatoire la facturation électronique pour les transactions B2B domestiques :

- **Septembre 2026** : toute entreprise doit être en mesure de **recevoir** des factures électroniques ; les grandes entreprises et les entreprises de taille intermédiaire (ETI) doivent également les **émettre**.
- **Septembre 2027** : l'émission devient obligatoire pour les PME et micro-entreprises.

Les factures B2B doivent transiter par une **Plateforme Agréée (PA)**, une plateforme habilitée par l'État, dans un format structuré : **Factur-X** (PDF avec XML embarqué), **UBL** ou **CII**. Pennylane est elle-même une PA agréée, si bien que les utilisateurs de Pennylane n'ont besoin d'aucune plateforme tierce. L'API expose l'ensemble du flux, et ce SDK le couvre intégralement.

## Vérifier vos enregistrements PA

```python
for registration in client.pa_registrations.list():
    print(registration)
```

## Envoyer une facture via le réseau PA

Finalisez la facture, puis transmettez-la à la plateforme :

```python
invoice = client.customer_invoices.finalize(draft.id)
client.customer_invoices.send_to_pa(invoice.id)
```

Suivez le statut de livraison soit via les champs de facturation électronique de la facture, soit via le flux de changements, soit avec l'événement webhook `customer_invoice.e_invoicing_status_updated` (voir le [guide des webhooks](webhooks.md)).

## Recevoir des factures électroniques fournisseurs

Les factures arrivant par le réseau atterrissent automatiquement dans Pennylane. Si vous recevez des factures structurées par un autre canal, importez-les :

```python
client.supplier_invoices.import_e_invoice(file="invoice.xml")
```

Les données Factur-X ou XML sont analysées de façon structurelle (pas d'OCR), ce qui garantit la fiabilité du fournisseur, des montants et des lignes.

## Importer des factures de vente électroniques depuis un autre outil

Si vous facturez depuis un ERP externe tout en gardant Pennylane comme système comptable et comme PA, poussez vos factures de vente en tant que factures électroniques :

```python
client.customer_invoices.import_e_invoice(
    file="factur-x.pdf",
    # invoice_options peut pré-remplir le client et les lignes, voir la docstring
)
```

## Mettre à jour le statut d'une facture électronique (avancé)

Les flux côté achats peuvent mettre à jour le statut de cycle de vie d'une facture électronique reçue (approuvée, refusée, paiement envoyé...) :

```python
client.supplier_invoices.update_e_invoice_status(invoice_id, ...)
```

!!! tip "Les échéances sont critiques pour l'activité"
    Si vous intégrez la facturation en vue de septembre 2026, testez le flux PA tôt, dans un environnement de test (sandbox). Le SDK lève une `ValidationError` accompagnée des détails de l'API lorsqu'un document ne respecte pas les exigences de format.
