top90Features = {
    'paymenttype',
    'pincodefirst2digits',
    'pincodealldigits',
    'promo_discount',
    'account_aspirationconversionratio',
    'latitude_recent',
    'historicalavgdeliveredfinalsalesamount',
    'finalsaleamount2',
    'longitude_recent',
    'adjustment_amount',
    'historical_avg_hourstorto_samevertical',
    'brand',
    'finalsaleamountold',
    'accountagedays',
    'uadevicefamily',
    'user_lockin_state',
    'color',
    'historical_stddev_hourstorto',
    'age_fsn',
    'historicalordersrtoratio',
    'fsn_discountperc_trend_future',
    'fsn_avg_price_last2days',
    'historicalordersnetdeliveredratio',
    'account_max_fsnage',
    'fsn_price_trend_vertical',
    'fsn_rtorate_last2days',
    'browse_pincode',
    'fsn_price_trend',
    'finalsaleamount',
    #'historicalavgdeliveredfinalsaleamountsameaddre...',
    'orderitemunitdiscountpercenatge',
    'fsn_discountperc_trend',
    'sla',
    'fsn_avg_discount_last2days',
    'account_dayssincelastorder',
    'historicalcancelled',
    'historicalrtoalphasellerperorderratio',
    'hourofday',
    'dayomonth',
    'marketingchannel',
    'historical_max_hourstorto',
    #'historicalmaxfinalsaleamountsameaddressid',
#     'account_min_fsnage',
#     'account_verticalaspirationconversionratio',
#     'account_avg_discount_amount',
#     'account_avg_fsnage',
#     'historicalrtopurchasedbymistakeperorderratio',
#     'historicalordersrvpratio',
#     'fsn_orders_last2days',
#     'minpurchaseamtinanycalendarmonth',
#     'historical_min_hourstorto',
#     'historical_avg_hourstorto',
#     'fsn_trend',
#     'fsn_discountperc_trend_vertical',
#     'account_avg_sla',
#     'historicalmaxfinalsaleamountalphaseller',
#     'historicalcodamountinflightorders',
#     'historicalavgfinalsaleamountsameaddressid',
#     'fsn_discountperc_trend_future_vertical',
#     'fsn_rto_trend',
#     'fsn_rvprate_last2days',
#     'historicalmaxfinalsaleamountsamevertical',
#     'certifiedbuyer_seller_rating_count',
#     'historicalrtoorcperorderratio',
#     'is_contact_active',
#     'fsn_rvp_trend',
#     'historicalminfinalsalesamount',
#     'historicalavgfinalsaleamountsamevertical',
#     'historicaltotalrvpsamesizeratio',
#     'account_stddev_fsnage',
#     'historicalorderstotalreturnratio',
#     'historicalmaxfinalsalesamount',
#     'avg_vertical_price_decile',
#     'historicalorderssamecolorratio',
#     'historicaldeliveredsameaddressid',
#     'historicalmaxdeliveredfinalsaleamountalphaseller',
#     'historicalavgfinalsalesamount',
#     'historicalcancelledsameverticalratio',
#     'seller_rating_nps',
#     'historicalorders_samevertical_last2hr',
#     'historicalavgdeliveredfinalsaleamountsamevertical',
#     'avgpurchaseamtinanycalendarmonth',
#     'category',
#     'historicalordersaddressid',
#     'historicalorders_last2hr',
#     'historicaldeliveredalphasellerperorderratio',
#     'account_daysbetweenfirstandlastorders',
#     'historicalcancelledsameaddressidperorderratio',
#     'account_selleraspirationconversionratio',
#     'dayofweek',
}



inplaceFeatures = {
    'paymenttype',
    'historicalcancelled',
    'pincodefirst2digits',
    'finalsaleamount',
    'business_unit',
    'dayomonth',
    'category',
    'historicalcancelledsameaddressid',
    'is_contact_active',
    'historical_avg_hourstorto',
    'historicaldeliveredsameaddressid',
    'historical_min_hourstorto',
    'historicalordersnetdeliveredratio',
    #'historicalavgdeliveredfinalsaleamountsameaddressid',
    'accountagedays',
    'account_dayssincelastorder',
    'orderitemunitdiscountpercenatge',
    'sla',
    'historicalorders',
    'historical_max_hourstorto',
    'hourofday',
    'saleschannel',
    'dayofweek',
    'account_avg_product_rating_count',
    'historicalcancelledsamevertical',
    'historicalminfinalsalesamount',
    'account_stddev_fsnage',
    'historicalorderstotalreturnratio',
    'repeatedorderssameproductonaccountid',
    'city_tier',
}

v1Features = {
    'category',
    'histinflightorders',
    'historicalcodamountinflightorders',
    'historicalinflightorderssameproduct',
    'historicalorders',
    'historicalordersnetdeliveredratio',
    'historicalordersrvpratio',
    'historicalorderssameverticalnetdeliveredratio',
    'historicalorderssameverticaltotalreturnratio',
    'historicalorderstotalreturnratio',
    'historicaltotalreturns',
    'isFKAssuered',
    'selling_price',
    'orderitemunitdiscountpercenatge',
    'paymenttype',
    'pincodefirst2digits',
    'repeatedorderssameproductonaccountid',
    'repeatedorderssameverticalonaccountid',
    'saleschannel',
    'shippingcharges',
    'sla',
    'returntype'
    #'orderdatekey'
}

allImplFeatures1 = v1Features.union(inplaceFeatures)
#allImplFeatures = allImplFeatures.union(top90Features)
#allImplFeatures.remove('historicalavgdeliveredfinalsaleamountsamevertical')
#allImplFeatures =set(list(v1Features)+list(inplaceFeatures)+list(top90Features))
allImplFeatures = top90Features
allImplFeatures.add('returntype')

def dropFeatures(EmeraldDf, select='all'):
    if select == 'all':
        pass
        columns = list(EmeraldDf.columns)
        drop_features = ['delivered', 'returntype2', 'returntype3', 'rvp', 'earlyrtoflag', 'intentcancellationranklabel',
                 'latertoflag','cancelled', 'logistics_vendor_id', 'earlycancellationflag', '6hrrtocancrank',
                '6hrrtocancbool', 'accuracy_level', 'event_info',
                'fsn', 'account_id', 'seller_id', 'ordertime',
                'latitude', 'longitude', 'orderitemid', 'checkout_id'] # remove orderdatekey at later stage
        columns = list(EmeraldDf.columns)
        for feature in drop_features:
        #print(feature)
            columns.remove(feature)
    
#     drop_features = {'isFKAssuered', 'historicalcancelledsameaddressid', 'selling_price', 'historicaltotalreturns', 'historicalcancelledsamevertical'}
    global allImplFeatures
#     drop_features = {'historicalcancelledsamevertical', 'historicalavgdeliveredfinalsaleamountsameaddre...', 'historicaltotalreturns', 'isFKAssuered', 'selling_price', 'historicalcancelledsameaddressid'}
#    allImplFeatures = allImplFeatures - drop_features
    columns = list(allImplFeatures)
    #columns.remove('historicalavgdeliveredfinalsaleamountsamevertical')


    EmeraldDf = EmeraldDf[columns]
    # df = df[df.vertical_name == 'shoe']

    # drop duplicate columns color_code
    # Finding duplicate column name
#     freq = {}
#     for col in EmeraldDf.columns:
#         freq[col] = freq.get(col, 0) + 1
#     duplicates = [col for col in freq if freq[col] > 1]

#     for col in duplicates:
#         EmeraldDf[col+"1"] = EmeraldDf[col].iloc[:, 0]
#         EmeraldDf.drop(col, axis=1, inplace=True)
    
    return EmeraldDf

def dropFeatures1(EmeraldDf, select='all'):
    if select == 'all':
        columns = list(EmeraldDf.columns)
        drop_features = ['delivered', 'returntype2', 'returntype3', 'rvp', 'earlyrtoflag', 'intentcancellationranklabel',
                 'latertoflag','cancelled', 'logistics_vendor_id', 'earlycancellationflag', '6hrrtocancrank',
                '6hrrtocancbool', 'accuracy_level', 'event_info',
                'fsn', 'account_id', 'seller_id', 'ordertime',
                'latitude', 'longitude', 'orderitemid', 'checkout_id'] # remove orderdatekey at later stage
        columns = list(EmeraldDf.columns)
        for feature in drop_features:
        #print(feature)
            columns.remove(feature)
    else:
        drop_features = {'isFKAssuered', 'historicalcancelledsameaddressid', 'selling_price', 'historicaltotalreturns', 'historicalcancelledsamevertical'}
        global allImplFeatures1
#     drop_features = {'historicalcancelledsamevertical', 'historicalavgdeliveredfinalsaleamountsameaddre...', 'historicaltotalreturns', 'isFKAssuered', 'selling_price', 'historicalcancelledsameaddressid'}
#    allImplFeatures = allImplFeatures - drop_features
        columns = list(allImplFeatures)
    #columns.remove('historicalavgdeliveredfinalsaleamountsamevertical')


    EmeraldDf = EmeraldDf[columns]
    # df = df[df.vertical_name == 'shoe']

    # drop duplicate columns color_code
    # Finding duplicate column name
#     freq = {}
#     for col in EmeraldDf.columns:
#         freq[col] = freq.get(col, 0) + 1
#     duplicates = [col for col in freq if freq[col] > 1]

#     for col in duplicates:
#         EmeraldDf[col+"1"] = EmeraldDf[col].iloc[:, 0]
#         EmeraldDf.drop(col, axis=1, inplace=True)
    
    return EmeraldDf