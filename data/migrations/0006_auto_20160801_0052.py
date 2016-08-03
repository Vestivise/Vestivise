# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-01 00:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_remove_yodleeaccount_annuitybalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account401kLoan',
            fields=[
                ('money_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='data.Money')),
                ('yodleeAccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account401kLoan', to='data.YodleeAccount')),
            ],
            bases=('data.money',),
        ),
        migrations.RemoveField(
            model_name='a401kloan',
            name='money_ptr',
        ),
        migrations.RemoveField(
            model_name='a401kloan',
            name='yodleeAccount',
        ),
        migrations.RemoveField(
            model_name='availablecash',
            name='account',
        ),
        migrations.AddField(
            model_name='availablecash',
            name='yodleeAccount',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='availableCash', to='data.YodleeAccount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='money',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 1, 0, 52, 53, 378992)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountamountdue',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountAmountDue', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='accountbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='accountlastpaymentamount',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountLastPayment', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='accountrefreshinfo',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountRefreshInfo', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='accountrewardbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountRewardBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='annuitybalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annuityBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='availablebalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availableBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='availablecredit',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availableCredit', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='availableloan',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availableLoan', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='historicalBalance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balance', to='data.HistoricalBalance'),
        ),
        migrations.AlterField(
            model_name='cash',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='cashvalue',
            name='yodleeAccount',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cashValue', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='costbasis',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costBasis', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='currentbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currentBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='employeecontribution',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employeeContribution', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='employercontribution',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employerContribution', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='escrowbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrowBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='faceamount',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faceAmount', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='grossexpenseamount',
            name='investmentOption',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grossExpenseAmount', to='data.InvestmentOption'),
        ),
        migrations.AlterField(
            model_name='holdingprice',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdingPrice', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='lastemployeecontributionamount',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lastEmployeeContributionAmount', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='lastpayment',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lastPayment', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='marginbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marginBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='matuityamount',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maturityAmount', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='minimumamountdue',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minimumAmountDue', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='moneymarketbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moneyMarketBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='netexpenseamount',
            name='investmentOption',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='netExpenseAmount', to='data.InvestmentOption'),
        ),
        migrations.AlterField(
            model_name='optionprice',
            name='investmentOption',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optionPrice', to='data.InvestmentOption'),
        ),
        migrations.AlterField(
            model_name='originalloanamount',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='originalLoanAmount', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='parvalue',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parValue', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='principalbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='principalBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='recurringpayment',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recurringPayment', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='runningbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runningBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='shortbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='spread',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spread', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='strikeprice',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strikePrice', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='totalcashlimit',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totalCashLimit', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='totalcreditlimit',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totalCreditLimit', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='totalcreditline',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totalCreditLine', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='totalunvestedbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totalUnvestedBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='totalvestedbalance',
            name='yodleeAccount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totalVestedBalance', to='data.YodleeAccount'),
        ),
        migrations.AlterField(
            model_name='unvestedvalue',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unvestedValue', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='value',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value', to='data.Holding'),
        ),
        migrations.AlterField(
            model_name='vestedvalue',
            name='holding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vestedValue', to='data.Holding'),
        ),
        migrations.DeleteModel(
            name='a401kLoan',
        ),
    ]