================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Prince Edward, Duke of Edinburgh (Edward Antony Richard Louis; born 10 March 1964), is a member of the British royal family.
He is the youngest child of Queen Elizabeth II and Prince Philip, Duke of Edinburgh, and the youngest sibling of King Charles III.
Edward was born third in the line of succession to the British throne and is 15th as of 2026.
Born at Buckingham Palace during the reign of his mother, Edward studied at Heatherdown School and completed his A-Levels at Gordonstoun before spending part of his gap year teaching at Whanganui Collegiate School in New Zealand.
Edward stepped down from the company in 2002 to begin full-time duties as a working member of the royal family and undertook engagements on behalf of his mother.
His charity work focuses on the arts, athletics, and the development of the Duke of Edinburgh's Award, which centres on fitness, wellbeing and community service.
Edward was given the title of Earl of Wessex prior to marrying Sophie Rhys-Jones in 1999.
Edward's mother conferred him the additional title of Earl of Forfar in 2019.
On Edward's 59th birthday in 2023, his brother Charles III granted him the title Duke of Edinburgh as a life peerage, a dukedom previously held by their father, who died in 2021, then briefly by Charles.
Early life and education

Edward was born at 8:20 pm on 10 March 1964 at Buckingham Palace, London, the third son and the fourth and youngest child of Queen Elizabeth II and Prince Philip, Duke of Edinburgh.
Edward was baptised on 2 May in the private chapel at Windsor Castle.
As with his three elder siblings, Charles, Anne, and Andrew, a governess oversaw his early education at Buckingham Palace before he attended Collingham College in Kensington, then known as Gibbs School.
In September 1972, Edward entered Heatherdown School, near Ascot in Berkshire.
At A-level, Edward obtained a C in English and two Ds in history and politics, and subsequently spent a gap year abroad, working for two terms as a house tutor and junior master at Wanganui Collegiate School in New Zealand.
On returning to the United Kingdom, Edward read history at Jesus College, Cambridge.
Post-university

Royal Marines

After graduating in 1986, Edward joined the Royal Marines, who had reportedly sponsored his tuition at Cambridge on the understanding that he would undertake future service.
Media reports suggested that Prince Philip, then  Captain General Royal Marines, was displeased, but Edward later stated that his father had not put undue pressure on him to reconsider and had supported his decision.
Others noted that Philip was, in fact, the most sympathetic family member toward his son's decision.
Buckingham Palace said that Edward's choice followed "much consideration" and that he was leaving with great regret, "but has concluded that he does not wish to make the service his long‐term career".
Theatre and television

After leaving military service, Edward opted to pursue a career in entertainment.
He commissioned the 1986 musical Cricket from Andrew Lloyd Webber and Tim Rice for his mother's 60th birthday celebration, which led to a job offer at Lloyd Webber's Really Useful Theatre Company.
Edward's first foray into television production was The Grand Knockout Tournament, informally known as It's a Royal Knockout, broadcast on 15 June 1987.
Four teams sponsored by Edward, his siblings Anne and Andrew, and Andrew's then wife, Sarah, competed for charity.
The programme attracted criticism from the media and the public, and it was later reported that the Queen had not been in favour of the event, with her courtiers having advised against it.
Ardent Productions

In 1993, Edward founded the television production company Ardent Productions.
Ardent produced a number of documentaries and dramas, but Edward was accused in the media of using his royal connections for financial gain.
Andy Beckett, writing in The Guardian, remarked that "to watch Ardent's few dozen hours of broadcast output is to enter a strange kingdom where every man in Britain still wears a tie, where pieces to camera are done in cricket jumpers, where people clasp their hands behind their backs like guardsmen.
Ardent's productions were better received in the United States, and a documentary Edward made in 1996 about his great-uncle Edward VIII (the Duke of Windsor) sold well internationally.
Nonetheless, the company reported losses every year it operated, except for one year in which Edward did not draw a salary.
In September 2001, an Ardent two‐man film crew allegedly invaded the privacy of Edward's nephew, Prince William, while he was studying at the University of St Andrews, in breach of industry guidelines concerning the privacy of members of the royal family.
William’s father, Edward's elder brother Charles, was reportedly angered by the incident.
In March 2002, Edward announced that he would step down as production director and joint managing director of Ardent to focus on his public duties and support the Queen during her Golden Jubilee year.
Marriage and children

Edward met Sophie Rhys-Jones in 1987 when he was dating one of her friends.
They met again in 1993 at a promotional shoot for the Prince Edward Summer Challenge, a charity event, and began their relationship soon afterwards.
In December 1993, amid growing speculation that they were planning to marry, Edward wrote to newspaper editors denying any wedding plans and asking the media to respect their privacy.
He proposed to Sophie while on holiday in the Bahamas in December 1998, and their engagement was announced on 6 January 1999.
Their wedding took place on 19 June 1999 in St George's Chapel at Windsor Castle.
The ceremony was a departure from the large, formal weddings of Edward's elder brothers at Westminster Abbey and St Paul's Cathedral, both of which had ended in divorce.
On his wedding day, Edward was created Earl of Wessex, with the subsidiary title of Viscount Severn (alluding to the Welsh roots of the Countess's family), breaking with the tradition that sons of the sovereign were created royal dukes.
Sophie experienced an ectopic pregnancy in 2001.
The couple have two children: Lady Louise Mountbatten-Windsor, born prematurely on 8 November 2003 following a sudden placental abruption; and James Mountbatten-Windsor (then Viscount Severn, now Earl of Wessex), born on 17 December 2007.
Since 2023, Edward's children have been styled as the children of a duke rather than as Prince or Princess and do not use the style of Royal Highness.
The family's country residence is Bagshot Park, while their office and official London home is at Buckingham Palace.
Edward's initial lease of Bagshot Park in 1998 was for 50 years at £5,000 a year, with the Crown Estate as landlord.
Approximately £3 million was spent on refurbishment, of which Edward paid £1.36 million, after which the rent rose to £90,000 a year.
In July 2023, the trust's remaining funds were transferred to the Edinburgh Trust No. 2, which had originally been set up in 1964.
Edward's patronages include the British Paralympic Association, the International Real Tennis Professionals Association, the Commonwealth Games Federation, BadmintonScotland, the Tennis and Rackets Association, the City of Birmingham Symphony Orchestra and Chorus, the London Mozart Players, Haddo House Choral and Operatic Society, Northern Ballet, the Edinburgh International Festival, the Royal Birmingham Conservatoire, the Production Guild, and National Youth Theatre.
The Earl of Wessex assumed many duties from his father, Prince Philip, as Philip reduced his commitments before retiring from royal duties.
Edward opened the 1990 Commonwealth Games in New Zealand and the 1998 Commonwealth Games in Malaysia, and in 2006 became vice-patron of Commonwealth Games Federation, taking on his father's ceremonial responsibilities; Philip had served as president.
He has also taken over his father's role in the Duke of Edinburgh's Award (DofE) scheme, attending Gold Award ceremonies around the world.
In September 2007, the Earl visited Israel in his capacity as Chairman of the International Council of the Duke of Edinburgh's Award to attend a number of events organised by the Israel Youth Award program, an affiliate of the Duke of Edinburgh's Award.
Edward had himself received the Award's gold medal in 1986 for "a 60-mile, four-day trek from Blair Atholl to Tomintoul" that he had planned.
Edward later became chair of trustees of the Duke of Edinburgh's International Award in 2015, and was named patron of the Duke of Edinburgh's Award in 2023.
Edward is also a trustee of the International Award Association, which "encompasses the DofE UK and all its other 61 National Award Authorities across the globe".
In 2018, Edward, as patron of the Tennis and Rackets Association, played on all 50 real tennis courts around the world and raised over £2 million for the Duke of Edinburgh's Award scheme.
In June 2011, Edward visited Baltimore to meet students and staff of the Living Classrooms Foundation and encourage their participation in the Duke of Edinburgh's Award's programme.
During the same trip, the couple travelled to Bahrain, where they received two gifts of jewels from the Bahraini royal family and Prime Minister.
In February and March 2012, the Earl and Countess visited the Caribbean as part of the Queen's Diamond Jubilee.
The Queen appointed the Earl of Wessex as Lord High Commissioner to the General Assembly of the Church of Scotland for 2014.
In 2015, in recognition of his contributions to projects associated with badminton, Edward received the President's Medal from the Badminton World Federation President Poul-Erik Høyer.
In May 2016, the Earl visited Ghana, where he joined President Mahama in presenting young people with the Head of State Awards for their participation in the Duke of Edinburgh's International Award Scheme.
In September 2016, Edward travelled to Chile as part of the Duke of Edinburgh's Award's diamond anniversary and visited projects run by the British and Commonwealth Fire and Rescue Company and Chilean-British Culture University, of which he is an honorary member and patron respectively.
The Earl and Countess of Wessex represented the Queen at the 50th anniversary celebrations of Sultan Hassanal Bolkiah's accession to the throne of Brunei in October 2017.
In April 2018, the Earl visited Australia to attend the XXI Commonwealth Games and to support fundraising events for participants in the Duke of Edinburgh Award challenges.
In July 2019, the Earl and Countess of Wessex visited Forfar on their first official visit to the royal burgh since the Queen granted Edward the additional title Earl of Forfar in March 2019.
In February 2022, Edward was appointed president of the Royal Windsor Horse Show, a position previously held by his father Prince Philip.
The following month, he visited Kenya to oversee the progress of the Duke of Edinburgh's International Award in the country.
In April 2022, the Earl and Countess of Wessex and Forfar toured Saint Lucia, Saint Vincent and the Grenadines, and Antigua and Barbuda to mark the Queen's Platinum Jubilee.
"


After he was created Duke of Edinburgh on his 59th birthday, Edward and Sophie visited Edinburgh to meet members of the Ukrainian and Eastern European communities in the city, including those displaced following the Russian invasion of Ukraine.
Edward became patron of the Duke of Edinburgh's Award upon being raised to the dukedom.
In 2024, he served as Lord High Commissioner to the General Assembly of the Church of Scotland, and was succeeded in the role the following year by Lady Elish Angiolini.
In 2025, Edward represented the King and the UK Government on several overseas trips, including a visit to Papua New Guinea to celebrate the 50th anniversary of independence, and a trip to Japan with Sophie.
In the media

In 1999, Edward was criticised by Labour MPs John Cryer and Lindsay Hoyle for comments he made during an interview with The New York Times, in which he stated that in Britain "They  hate anyone who succeeds" and "America is where the money is".
In 2011, close associates of Jonathan Rees, a private investigator connected to the News International phone hacking scandal, alleged that he had accessed the bank accounts of Edward and Sophie and sold information about them to the Sunday Mirror.
Titles, styles, honours and arms

Titles and styles

Until his marriage, Edward was known as "His Royal Highness The Prince Edward".
On 19 June 1999, he became "His Royal Highness The Earl of Wessex".
At the time of his marriage, Buckingham Palace announced the intention that Edward would eventually be created Duke of Edinburgh, a title then held by his father, Prince Philip, once it had merged in the Crown following the death of both his parents.
On 10 March 2019, his 55th birthday, Edward was granted the additional title of Earl of Forfar for use in Scotland.
On his 59th birthday, 10 March 2023, Edward was created Duke of Edinburgh, thus becoming "His Royal Highness The Duke of Edinburgh".
In 1994, the Independent Royalist Party of Estonia, which aspired to establish a monarchy in the country, sent a letter to Queen Elizabeth II requesting permission to crown Edward as King of Estonia.
The letter described Edward as a "young British prince much admired by Estonians", and stated that the party "would be most honoured if you would accept this rare request".
Buckingham Palace declined, calling it "a charming idea but a rather unlikely one".
Honours

Edward is a Royal Knight Companion of the Most Noble Order of the Garter, an Extra Knight of the Most Ancient and Most Noble Order of the Thistle, a Knight Grand Cross of the Royal Victorian Order, and a Personal Aide-de-Camp to the Sovereign.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (cd09bda1-71b3-4e5a-83f6-7531efda8997)
 Call ID: cd09bda1-71b3-4e5a-83f6-7531efda8997
  Args:
    source: Prince_Edward
    type: :Man
  AssignClass (1157207a-89e2-4857-b004-7e3395be763a)
 Call ID: 1157207a-89e2-4857-b004-7e3395be763a
  Args:
    type: :Person
    source: Prince_Edward
  AddLiteral (f019b5fb-d411-4180-8936-dbeaa6e1c9f3)
 Call ID: f019b5fb-d411-4180-8936-dbeaa6e1c9f3
  Args:
    source: Prince_Edward
    literal_value: 1964
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (fe3bc92f-d217-4d4d-bb2d-5f17262c9359)
 Call ID: fe3bc92f-d217-4d4d-bb2d-5f17262c9359
  Args:
    type: :Woman
    source: Queen_Elizabeth_II
  AssignClass (0c6db189-07a8-4f47-82d5-9ce01edfc0a4)
 Call ID: 0c6db189-07a8-4f47-82d5-9ce01edfc0a4
  Args:
    source: Queen_Elizabeth_II
    type: :Person
  AssignClass (840b1641-d310-4421-907a-852c13666123)
 Call ID: 840b1641-d310-4421-907a-852c13666123
  Args:
    type: :Man
    source: Prince_Philip
  AssignClass (f946d332-70fd-462d-aac4-3d765c51db7c)
 Call ID: f946d332-70fd-462d-aac4-3d765c51db7c
  Args:
    source: Prince_Philip
    type: :Person
  AddTriple (0b66692c-0ca7-4049-a10a-adb385fce277)
 Call ID: 0b66692c-0ca7-4049-a10a-adb385fce277
  Args:
    target: Queen_Elizabeth_II
    relation: :hasMother
    source: Prince_Edward
  AddTriple (9ae589e2-2e17-42dd-95b0-b806c461ad59)
 Call ID: 9ae589e2-2e17-42dd-95b0-b806c461ad59
  Args:
    relation: :hasFather
    target: Prince_Philip
    source: Prince_Edward
  AssignClass (e3f428ea-8c00-407f-9ca2-1b03c664b206)
 Call ID: e3f428ea-8c00-407f-9ca2-1b03c664b206
  Args:
    type: :Man
    source: King_Charles_III
  AssignClass (3e7ee824-80e6-4c84-b539-09aa98da74f7)
 Call ID: 3e7ee824-80e6-4c84-b539-09aa98da74f7
  Args:
    type: :Person
    source: King_Charles_III,type:
  AddTriple (17bfcad4-b6f8-430f-847a-821e6bb9a57a)
 Call ID: 17bfcad4-b6f8-430f-847a-821e6bb9a57a
  Args:
    source: Prince_Edward
    relation: :isBrotherOf
    target: King_Charles_III
  AssignClass (737b1ae2-524d-4d59-9205-d501231f1bb2)
 Call ID: 737b1ae2-524d-4d59-9205-d501231f1bb2
  Args:
    source: Sophie_Rhys-Jones
    type: :Woman
  AssignClass (e114aa73-14fa-4684-b8c8-5f6c9088a45c)
 Call ID: e114aa73-14fa-4684-b8c8-5f6c9088a45c
  Args:
    type: :Person
    source: Sophie_Rhys-Jones
  AddLiteral (69043297-d9c8-4118-8aa1-b1d38cc95e65)
 Call ID: 69043297-d9c8-4118-8aa1-b1d38cc95e65
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Edward
    literal_value: 1999
  AddTriple (ca019117-8f20-41da-b28b-bb26845ba482)
 Call ID: ca019117-8f20-41da-b28b-bb26845ba482
  Args:
    source: Prince_Edward
    relation: :hasRelation
    target: Sophie_Rhys-Jones
  AssignClass (0317b20b-cfcc-4e03-947a-610572eddb80)
 Call ID: 0317b20b-cfcc-4e03-947a-610572eddb80
  Args:
    type: :Woman
    source: Lady_Louise_Mountbatten-Windsor
  AssignClass (ca9d69ef-2853-4a11-8679-03fed1e84671)
 Call ID: ca9d69ef-2853-4a11-8679-03fed1e84671
  Args:
    type: :Person
    source: Lady_Louise_Mountbatten-Windsor
  AddTriple (be01671b-2419-4c28-8246-b3e5ad6d2430)
 Call ID: be01671b-2419-4c28-8246-b3e5ad6d2430
  Args:
    source: Lady_Louise_Mountbatten-Windsor
    target: Prince_Edward
    relation: :isChildOf
  AddTriple (7f6fad77-6468-42cf-9e46-c9448bb114c5)
 Call ID: 7f6fad77-6468-42cf-9e46-c9448bb114c5
  Args:
    relation: :isChildOf
    target: Sophie_Rhys-Jones
    source: Lady_Louise_Mountbatten-Windsor
  AssignClass (c1499a0f-06e5-4cb9-9208-2aee83dac96e)
 Call ID: c1499a0f-06e5-4cb9-9208-2aee83dac96e
  Args:
    type: :Man
    source: James_Mountbatten-Windsor
  AssignClass (eda3da8e-27a5-4ea1-ab80-c785c55d2b14)
 Call ID: eda3da8e-27a5-4ea1-ab80-c785c55d2b14
  Args:
    type: :Person
    source: James_Mountbatten-Windsor
  AddTriple (3275a257-8bf9-4a4f-81a0-dad7e75bbcba)
 Call ID: 3275a257-8bf9-4a4f-81a0-dad7e75bbcba
  Args:
    target: Prince_Edward
    relation: :isChildOf
    source: James_Mountbatten-Windsor
  AddTriple (88c2eb74-df3b-4ba3-8ae1-bfb86a3441c8)
 Call ID: 88c2eb74-df3b-4ba3-8ae1-bfb86a3441c8
  Args:
    source: James_Mountbatten-Windsor
    target: Sophie_Rhys-Jones
    relation: :isChildOf
  AssignClass (53818be2-f12e-46de-94f7-466673475342)
 Call ID: 53818be2-f12e-46de-94f7-466673475342
  Args:
    type: :Woman
    source: Anne
  AssignClass (4b77a9f3-caca-4104-b925-9f3d03d0ad55)
 Call ID: 4b77a9f3-caca-4104-b925-9f3d03d0ad55
  Args:
    source: Anne
    type: :Person
  AddTriple (6cdf7615-fdd3-44c8-96db-5f1b140506c3)
 Call ID: 6cdf7615-fdd3-44c8-96db-5f1b140506c3
  Args:
    source: Anne
    target: Prince_Edward
    relation: :isSisterOf
  AssignClass (bba1bccd-81d6-4237-8cf9-e6d08f8e1f1d)
 Call ID: bba1bccd-81d6-4237-8cf9-e6d08f8e1f1d
  Args:
    type: :Man
    source: Andrew
  AssignClass (b614d506-db06-4ca4-a6b9-f722aec318bd)
 Call ID: b614d506-db06-4ca4-a6b9-f722aec318bd
  Args:
    type: :Person
    source: Andrew
  AddTriple (6327cc13-e7c0-4361-aa34-4c244e911b52)
 Call ID: 6327cc13-e7c0-4361-aa34-4c244e911b52
  Args:
    relation: :isBrotherOf
    target: Prince_Edward
    source: Andrew
  AssignClass (05da80c1-8369-4b58-8f02-76c81ce48788)
 Call ID: 05da80c1-8369-4b58-8f02-76c81ce48788
  Args:
    source: Prince_William
    type: :Man
  AssignClass (5ff788a2-8615-49f8-a16e-ca18acdcc20e)
 Call ID: 5ff788a2-8615-49f8-a16e-ca18acdcc20e
  Args:
    type: :Person
    source: Prince_William
  AddTriple (44f0738f-ce66-45ce-a0de-8c3163b159b5)
 Call ID: 44f0738f-ce66-45ce-a0de-8c3163b159b5
  Args:
    source: Prince_William
    target: King_Charles_III
    relation: :isChildOf
  AssignClass (180c223a-be7b-4389-abfe-7fcc1477055d)
 Call ID: 180c223a-be7b-4389-abfe-7fcc1477055d
  Args:
    type: :Woman
    source: Sarah
  AssignClass (b5e3ed1a-4c20-4b15-a27f-0dd7ca0ad0d0)
 Call ID: b5e3ed1a-4c20-4b15-a27f-0dd7ca0ad0d0
  Args:
    source: Sarah
    type: :Person
  AddTriple (60783e34-6854-4800-a799-b6c00b7acc2d)
 Call ID: 60783e34-6854-4800-a799-b6c00b7acc2d
  Args:
    target: Andrew
    relation: :hasRelation
    source: Sarah
  AddLiteral (a31384b7-72ac-472f-986f-0bbfe872496f)
 Call ID: a31384b7-72ac-472f-986f-0bbfe872496f
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Philip
    literal_value: 2021
  Finish (55e5681d-b233-46f6-9961-a10ea2ea543c)
 Call ID: 55e5681d-b233-46f6-9961-a10ea2ea543c
  Args: