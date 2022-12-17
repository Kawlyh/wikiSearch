#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

import beans as beans
from beans import DBExecute as dbe

global sssid
sssid = 3453540


def getsnak(snakid, mainsnak, pid, rhash=None):
    # mainsnak
    mainsnak_snaktype = mainsnak.get('snaktype')
    mainsnak_property = mainsnak.get('property')
    mainsnak_datavalue = mainsnak.get('datavalue')
    if mainsnak_snaktype == 'value':
        mainsnak_datatype = mainsnak_datavalue.get('type')

        snakb = beans.sank(snakid=snakid, stype=mainsnak_snaktype,
                           datatype=mainsnak_datatype)
        dbe().addToCom(snakb, ['snak', 'snakid', snakid])
        if mainsnak_datatype == 'string' or mainsnak_datatype == 'external-id':
            value = mainsnak_datavalue.get('value')

            string = beans.string(snakid=snakid, pid=pid, hashv=rhash,
                                  value=value)
            dbe().addTo(string, ['string', 'snakid', snakid])
        elif mainsnak_datatype == 'monolingualtext':
            mainsnak_datavalue = mainsnak_datavalue.get('value')
            language = mainsnak_datavalue.get('language')
            text = mainsnak_datavalue.get('text')

            monotext = beans.monotext(snakid=snakid, pid=pid, hashv=rhash,
                                      language=language, text=text)
            dbe().addTo(monotext, ['monotext', 'snakid', snakid])
        elif mainsnak_datatype == 'wikibase-entityid':
            mainsnak_datavalue = mainsnak_datavalue.get('value')
            entitytype = mainsnak_datavalue.get('entity-type')
            entityid = mainsnak_datavalue.get('id')
            entitynumeric = mainsnak_datavalue.get('numeric-id')

            entity = beans.entityid(snakid=snakid, pid=pid, hashv=rhash,
                                    entitytype=entitytype,
                                    entityid=entityid, numericid=entitynumeric)
            dbe().addTo(entity, ['entityid', 'snakid', snakid])
        elif mainsnak_datatype == 'globecoordinate':
            mainsnak_datavalue = mainsnak_datavalue.get('value')
            latitude = mainsnak_datavalue.get('latitude')
            longitude = mainsnak_datavalue.get('longitude')
            altitude = mainsnak_datavalue.get('altitude')
            precision = mainsnak_datavalue.get('precision')
            globe = mainsnak_datavalue.get('globe')

            globe = beans.globecoordinate(
                    snakid=snakid, pid=pid, hashv=rhash, latitude=latitude,
                    longitude=longitude, altitude=altitude,
                    precision=precision, globe=globe)
            dbe().addTo(globe, ['globecoordinate', 'snakid', snakid])
        elif mainsnak_datatype == 'quantity':
            mainsnak_datavalue = mainsnak_datavalue.get('value')
            amount = mainsnak_datavalue.get('amount')
            upperbound = mainsnak_datavalue.get('upperBound')
            lowerbound = mainsnak_datavalue.get('lowerBound')
            unit = mainsnak_datavalue.get('unit')

            quantity = beans.quantity(
                    snakid=snakid, pid=pid, hashv=rhash,
                    amount=amount, upperbound=upperbound,
                    lowerbound=lowerbound, unit=unit)
            dbe().addTo(quantity, ['quantity', 'snakid', snakid])
        elif mainsnak_datatype == 'time':
            mainsnak_datavalue = mainsnak_datavalue.get('value')
            time = mainsnak_datavalue.get('time')
            timezone = mainsnak_datavalue.get('timezone')
            before = mainsnak_datavalue.get('before')
            after = mainsnak_datavalue.get('after')
            precision = mainsnak_datavalue.get('precision')
            calendarmodel = mainsnak_datavalue.get('calendarmodel')

            ttime = beans.time(
                    snakid=snakid, pid=pid, hashv=rhash, ttime=time,
                    timezone=timezone, before=before, after=after,
                    precision=precision, calendarmodel=calendarmodel)
            dbe().addTo(ttime, ['time', 'snakid', snakid])
        else:
            print(mainsnak_datatype)
            print(mainsnak_datavalue)
            print('what !')

    else:
        snakb = beans.sank(
                snakid=snakid, stype=mainsnak_snaktype, datatype=None)
        dbe().addToCom(snakb, ['snak', 'snakid', snakid])


def gensnakid():
    global sssid
    '''
    查表生成snakid
    sid = dbe().query('select 0+snakid as snakid from snak order by snakid desc limit 1')
    if len(sid) < 1:
        return '0'
    else:
        snid = sid.iloc[0].at['snakid']
        return str(int(snid) + 1)
    '''
    sssid += 1
    return sssid


def main():
    infile = open("wikidata-seg000.json", 'r', encoding="utf-8")
    # 读入多少行
    lineNums = 1000000
    for i in range(lineNums):
        if i % 100 == 0:
            starttime = time.clock()
        print('导入第 {} 条数据'.format(i))
        line = infile.readline()
        # 跳过第一行的 [
        if i < 61716:
            continue
        # 删去末尾的,
        line = line[:-2]
        line = json.loads(line)

        top_id = line.get('id')
        top_type = line.get('type')
        top_pageid = line.get('pageid')
        top_ns = line.get('ns')
        top_title = line.get('title')
        top_lastrevid = line.get('lastrevid')
        top_modified = line.get('modified')

        entity = beans.entity(eid=top_id, etype=top_type, epageid=top_pageid,
                              ens=top_ns, etitle=top_title,
                              elastrevid=top_lastrevid, emodified=top_modified)
        dbe().addTo(entity, ['entity', 'eid', top_id])

        # labels
        top_labels = line.get('labels')
        for top_label_key in top_labels.keys():
            # labels的语言
            top_labels_language = top_label_key
            # labels的值
            top_labels_value = top_labels.get(top_label_key).get('value')

            labels = beans.labels(eid=top_id, language=top_labels_language,
                                  value=top_labels_value)
            dbe().addTo(labels, ['labels', 'lid', -1])

        # sitelinks
        top_sitelinks = line.get('sitelinks')
        for top_sitelinks_key in top_sitelinks.keys():
            # sitelinks的site
            top_sitelinks_site = top_sitelinks_key
            # sitelinks的title
            top_sitelinks_title = top_sitelinks.get(top_sitelinks_key).get('title')
            # sitelinks的badges
            top_sitelinks_badges = top_sitelinks.get(top_sitelinks_key).get('badges')
            top_sitelinks_badges = ','.join(top_sitelinks_badges)
            # sitelinks的url
            top_sitelinks_url = top_sitelinks.get(top_sitelinks_key).get('url')

            sitelinks = beans.sitelinks(eid=top_id, site=top_sitelinks_site,
                                        title=top_sitelinks_title,
                                        badges=top_sitelinks_badges,
                                        url=top_sitelinks_url)
            dbe().addTo(sitelinks, ['sitelinks', 'sid', -1])

        # descriptions
        top_descriptions = line.get('descriptions')
        for top_descriptions_key in top_descriptions.keys():
            # descriptions的language
            top_descriptions_language = top_descriptions_key
            # descriptions的 value
            top_descriptions_value = top_descriptions.get(top_descriptions_key).get('value')

            descriptions = beans.descriptions(eid=top_id,
                                              language=top_descriptions_language,
                                              value=top_descriptions_value)
            dbe().addTo(descriptions, ['descriptions', 'did', -1])

        # aliases
        top_aliases = line.get('aliases')
        for top_aliases_key in top_aliases.keys():
            # aliases的 language
            top_aliases_language = top_aliases_key
            # aliases的 value
            top_aliases_value = top_aliases.get(top_aliases_key)
            top_aliases_value = [x.get('value') for x in top_aliases_value]
            top_aliases_value = ','.join(top_aliases_value)

            aliases = beans.aliases(eid=top_id,
                                    language=top_aliases_language,
                                    value=top_aliases_value)
            dbe().addTo(aliases, ['aliases', 'aid', -1])

        # claims
        top_claims = line.get('claims')
        # property
        for top_claims_key in top_claims.keys():
            top_claims_snaks_to_same_property = top_claims.get(top_claims_key)
            # all statements
            for snak in top_claims_snaks_to_same_property:
                statements_id = snak.get('id')
                statements_type = snak.get('type')
                statements_rank = snak.get('rank')

                mainsnak = snak.get('mainsnak')
                snid = gensnakid()
                statements = beans.statements(
                        sid=statements_id, pid=top_claims_key,
                        snakid=snid, stype=statements_type,
                        srank=statements_rank, eid=top_id)
                dbe().addTo(statements, ['statements', 'sid', statements_id])

                getsnak(snid, mainsnak, top_claims_key)

                # references
                mainsnak_references = snak.get('references')
                if mainsnak_references is not None:
                    for mainsnak_refer in mainsnak_references:
                        refer_hash = mainsnak_refer.get('hash')
                        refer_snaks = mainsnak_refer.get('snaks')
                        for key in refer_snaks.keys():
                            ma_refer_snaks = refer_snaks.get(key)
                            for refer_snak in ma_refer_snaks:
                                snid = gensnakid()
                                references = beans.references(
                                        sid=statements_id,
                                        snakid=snid,
                                        eid=top_id)
                                dbe().addTo(references,
                                            ['refer', 'rid', -1])
                                # print('refer snak')
                                getsnak(snid, refer_snak, key, refer_hash)
                else:
                    pass

                # qualifiers
                mainsnak_qualifiers = snak.get('qualifiers')
                if mainsnak_qualifiers is not None:
                    for key in mainsnak_qualifiers.keys():
                        mainsnak_snaks = mainsnak_qualifiers.get(key)
                        for mainsnak_snak in mainsnak_snaks:
                            qual_hash = mainsnak_snak.get('hash')
                            snid = gensnakid()
                            qualifiers = beans.qualifiers(
                                    sid=statements_id, snakid=snid,
                                    eid=top_id)
                            dbe().addTo(qualifiers,
                                        ['qualifiers', 'qid', -1])
                            # print('qual snak')
                            getsnak(snid, mainsnak_snak, key, qual_hash)
                else:
                    pass
        dbe().comm()
        endtime = time.clock()
        if i % 100 == 0:
            print('     用时: {} s'.format(endtime - starttime))


if __name__ == "__main__":
    main()
