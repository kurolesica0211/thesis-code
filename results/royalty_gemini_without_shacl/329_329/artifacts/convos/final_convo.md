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
King Juan Carlos IQueen Sofía


The Duchess of Soria and HernaniThe Duke of Soria and Hernani


The Dowager Duchess of Calabria


Infanta Elena, Duchess of Lugo (Elena María Isabel Dominica de Silos de Borbón y de Grecia; born 20 December 1963), is the first child and eldest daughter of King Juan Carlos I and Queen Sofía.
As the eldest sister of King Felipe VI, Elena is the third in the line of succession to the Spanish throne, behind her nieces, Leonor, Princess of Asturias and Infanta Sofía.
She has a younger sister, Infanta Cristina.
On 3 March 1995, on the occasion of her marriage to Jaime de Marichalar y Sáenz de Tejada, Lord of Tejada, her father gave her the title of Duchess of Lugo.
Since the ascension of her younger brother to the Spanish throne, Elena has not been part of the royal family.
Early life and family

Infanta Elena was born on 20 December 1963 at Our Lady of Loreto Sanatorium, now known as ORPEA Madrid Loreto, in Madrid.
She is the first member to be born in a hospital from King Juan Carlos
I's family and the eldest child of Juan Carlos I, the former Spanish monarch, and Queen Sofía (born Princess of Greece and Denmark).
Elena studied at Santa María del Camino School in Madrid and got a diploma as a secondary school teacher in 1986, with a specialty in English studies.
Equestrianism

From her childhood, Elena had a love of horse riding, a passion that she inherited from her grandmother, Princess María de las Mercedes, Countess of Barcelona.
Afterwards, in the late 1980s, King Juan Carlos ordered the construction of stables and a riding arena at the Royal Palace of Zarzuela so that his daughter could practice her hobby in the palace.
Elena was described by fellow equestrian
Luis Jaime Carvajal y Salas, 5th Duke of Aveyro, as a "very good " but he pointed that her problem was that horse riding "requires time and she doesn't have it" as a member of the royal family.
Some of the Infanta's most notable horses are Qant (her favorite horse since 2011) and Jordano EB (Qant's successor), a chestnut horse that she bred herself.
As of 2016, Elena owned at least eight horses.
Elena has had several equestrian teachers, but no official one since she left the royal family.
The most important are Felipe de Zuleta y Alejandro from 2006 to 2015, an official of the Royal Guard and brother of the Duke of Abrantes, private secretary of Queen Letizia from 2014 to 2024, and Luis Astolfi Pérez de Guzmán, a former boyfriend and currently a close friend of hers.
Luis and Elena rekindled their friendship in 2013 after many years with no contact.
She shares this hobby with her daughter, Victoria, Grandee of Spain, as well as watching bullfighting.
Marriage and children

Elena met Jaime de Marichalar y Sáenz de Tejada, Lord of Tejada, son of the Amalio de Marichalar y Bruguera, 8th Count of Ripalda, for the first time in 1987 in Paris.
Elena was studying French literature in the French capital while Jaime was working for Credit Suisse.
In addition to the immediate royal family, Princess María de las Mercedes, Countess of Barcelona (the bride's grandmother), Infanta Pilar, Duchess of Badajoz (the bride's aunt) and the Duchess and Duke of Soria (the bride's aunt and uncle) were present.
It was the first royal wedding in Spain since the wedding of King Alfonso XIII and Princess Victoria Eugenie of Battenberg in 1906.
Also, to celebrate the occasion, King Juan Carlos gave Infanta Elena the title of Duchess of Lugo.
The couple has two children: Felipe de Marichalar y Borbón (born 17 July 1998) and Victoria de Marichalar y Borbón (born 9 September 2000) were born at Ruber International Hospital in Madrid.
On 26 June 2003, a few days after the king announced his daughter's third pregnancy, Elena suffered a miscarriage.
As children of an Infanta of Spain, Elena's children are Grandees of Spain.
On 13 November 2007, it was announced that Elena had separated from her husband.
The Duchess and Duke consort of Lugo were divorced in December 2009.
On 21 January 2010, the divorce was registered at the Civil Registry of the Spanish Royal Family and it was officially announced on 9 February 2010; Jaime de Marichalar was no longer permitted to use the ducal title nor was he considered an official member of the Spanish Royal Family.
Activities and personal work

Elena started to attend official events at a very young age.
Since finishing her basic education in 1983, Elena, along with her sister Cristina, has supported their parents.
They represented the Crown at official events such as the National Day, the wedding of Princess Astrid of Belgium, the re-burial of Queen Victoria Eugenia at El Escorial, the state visit of Mexican president Miguel de la Madrid to Spain, and the 1984 Prince of Asturias Awards ceremony, among others.
Since her brother's ascension to the throne in June 2014 and her departure from the royal family, Elena has reduced her public appearances.
However, that year she did represent the Crown at some events, such as the funeral of Cayetana Fitz-James Stuart, 18th Duchess of Alba in November 2014 and the presentation of the National Sports Awards in December 2014.
Since then, Elena has limited her institutional activity to annually presiding over the awards ceremony for the Patrimonio Nacional's Children's and Youth Painting Contest.
In addition to her obligations as an infanta, Elena has a job that allows her to compensate for the lack of public salary by not being a member of the royal family.
Elena has worked at the Mapfre Foundation since 2008 and currently serves as director of social and cultural projects.
In this role, Elena has helped the foundation to promote projects and give visibility to various cooperation programs in Latin America through several international tours.



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
  AssignClass (d8519fc2-d36b-4dd7-93ee-cd19dbb60c05)
 Call ID: d8519fc2-d36b-4dd7-93ee-cd19dbb60c05
  Args:
    source: Juan_Carlos_I
    type: :Man
  AssignClass (3621ddd1-db99-4f08-8fd0-9bb6dcd37e10)
 Call ID: 3621ddd1-db99-4f08-8fd0-9bb6dcd37e10
  Args:
    type: :Woman
    source: Sofia
  AssignClass (12a1e1e7-0b29-463b-b972-c52d58dcc12b)
 Call ID: 12a1e1e7-0b29-463b-b972-c52d58dcc12b
  Args:
    type: :Woman
    source: Elena_de_Borbon
  AssignClass (b0ea2493-8e41-44cf-9fbc-39893f3a9653)
 Call ID: b0ea2493-8e41-44cf-9fbc-39893f3a9653
  Args:
    type: :Man
    source: Felipe_VI
  AssignClass (1b6ad52d-f905-4f05-bc6f-7891b61ea2f3)
 Call ID: 1b6ad52d-f905-4f05-bc6f-7891b61ea2f3
  Args:
    type: :Woman
    source: Cristina_de_Borbon
  AssignClass (ca2ae7ac-40d1-496d-8d5e-105f08065e41)
 Call ID: ca2ae7ac-40d1-496d-8d5e-105f08065e41
  Args:
    source: Jaime_de_Marichalar
    type: :Man
  AssignClass (3d6d49cd-5320-4cf3-acbd-63416809f2dd)
 Call ID: 3d6d49cd-5320-4cf3-acbd-63416809f2dd
  Args:
    type: :Man
    source: Felipe_de_Marichalar
  AssignClass (5512655f-e325-45d7-8043-032b5bfeea21)
 Call ID: 5512655f-e325-45d7-8043-032b5bfeea21
  Args:
    type: :Woman
    source: Victoria_de_Marichalar
  AddTriple (0e68b3ea-75d6-4777-95f3-3927a88d561b)
 Call ID: 0e68b3ea-75d6-4777-95f3-3927a88d561b
  Args:
    relation: :isFatherOf
    target: Elena_de_Borbon
    source: Juan_Carlos_I
  AddTriple (c305bd17-372d-44d3-a2b5-102703c6281f)
 Call ID: c305bd17-372d-44d3-a2b5-102703c6281f
  Args:
    source: Sofia
    target: Elena_de_Borbon
    relation: :isMotherOf
  AddTriple (34bf1144-3f62-4762-83d7-70695110b345)
 Call ID: 34bf1144-3f62-4762-83d7-70695110b345
  Args:
    target: Felipe_VI
    relation: :isFatherOf
    source: Juan_Carlos_I
  AddTriple (38d423f0-2970-4253-bf76-954cff368d11)
 Call ID: 38d423f0-2970-4253-bf76-954cff368d11
  Args:
    source: Sofia
    relation: :isMotherOf
    target: Felipe_VI
  AddTriple (f37be3f3-5536-457c-a3cc-1ff6101e4311)
 Call ID: f37be3f3-5536-457c-a3cc-1ff6101e4311
  Args:
    relation: :isFatherOf
    target: Cristina_de_Borbon
    source: Juan_Carlos_I
  AddTriple (2a126b41-c758-4ebf-9166-8c1b2e07b3fe)
 Call ID: 2a126b41-c758-4ebf-9166-8c1b2e07b3fe
  Args:
    source: Sofia
    target: Cristina_de_Borbon
    relation: :isMotherOf
  AddTriple (16a766e4-8f09-46f5-b181-dc6c5d3ecb4f)
 Call ID: 16a766e4-8f09-46f5-b181-dc6c5d3ecb4f
  Args:
    target: Felipe_de_Marichalar
    relation: :isFatherOf
    source: Jaime_de_Marichalar
  AddTriple (e13f723e-adb8-405d-b9b0-92340993d18c)
 Call ID: e13f723e-adb8-405d-b9b0-92340993d18c
  Args:
    source: Elena_de_Borbon
    relation: :isMotherOf
    target: Felipe_de_Marichalar
  AddTriple (ca37a28f-f447-4305-a774-a0b38200eba2)
 Call ID: ca37a28f-f447-4305-a774-a0b38200eba2
  Args:
    target: Victoria_de_Marichalar
    relation: :isFatherOf
    source: Jaime_de_Marichalar
  AddTriple (ca990589-849e-4135-a467-ecd1f112b7cc)
 Call ID: ca990589-849e-4135-a467-ecd1f112b7cc
  Args:
    source: Elena_de_Borbon
    relation: :isMotherOf
    target: Victoria_de_Marichalar
  AddLiteral (e241c592-4579-492d-8cc9-414e3f48091b)
 Call ID: e241c592-4579-492d-8cc9-414e3f48091b
  Args:
    source: Elena_de_Borbon
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1963
  AddLiteral (179a0d53-6aa8-407a-af87-bda83600f628)
 Call ID: 179a0d53-6aa8-407a-af87-bda83600f628
  Args:
    source: Felipe_de_Marichalar
    literal_value: 1998
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (299798cd-321d-49dc-b55c-1d94c549037c)
 Call ID: 299798cd-321d-49dc-b55c-1d94c549037c
  Args:
    source: Victoria_de_Marichalar
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 2000
  AddLiteral (0f440897-9f16-4c2b-9777-86be4b560c58)
 Call ID: 0f440897-9f16-4c2b-9777-86be4b560c58
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1995
    source: Elena_de_Borbon
  Finish (7527e862-8c3e-472a-98d3-deedf854db4e)
 Call ID: 7527e862-8c3e-472a-98d3-deedf854db4e
  Args: