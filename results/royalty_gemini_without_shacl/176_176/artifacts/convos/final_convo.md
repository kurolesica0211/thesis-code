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
The Custodian of the Crown  Prince Radu


Princess Elena 
Princess Irina 
Princess Sophie 
Princess Maria 


Princess Elena of Romania (born 15 November 1950) is the second daughter of King Michael I and Queen Anne of Romania.
Elena is first in the line of succession to the former Romanian throne and headship of the House of Romania as her elder sister Margareta's heir presumptive.
Early life

Birth

Elena was born on 15 November 1950 at Clinique de Montchoisi in Lausanne, Switzerland as the second daughter of King Michael I and Queen Anne.
She was baptised in the Orthodox faith; her godmothers were her paternal grandmother Helen, Queen Mother of Romania (who was also her namesake) and also Queen Mary of the United Kingdom.
Childhood

Elena spent her childhood at her family homes in Lausanne, Switzerland, and in the United Kingdom at Ayot House, St Lawrence, Hertfordshire; during holidays she and her sisters spent time with their grandmother, Helen, Queen Mother in Florence, Italy at Villa Sparta and in Denmark with Princess Margaret and Prince René.
Education

Elena received her primary education in Switzerland and her secondary at Effingham House in Little Common, Bexhill-on-Sea, East Sussex; she was fond of sports during her school years, playing on goal defence in the netball team.
Careers

In the mid-1970s, Elena taught handicapped children for a short period of time in London and after her leaving, she began a two-year course in art restoration; following the end of her course she worked in an art restoration firm in London.
Activities

In the 1980s Elena along with her first husband Robin Medforth-Mills started a project to train 45 handicapped Ethiopian refugees in printing, bookbinding and leatherwork.
In 1982 Elena founded an International school in Gezira, Sudan.
In 1990 along with Elena’s first husband, the then-Lord Mayor of Newcastle, Terry Cooney, and Harry Charrington was a founder-member of the North-East Relief Fund for Romania, which helped victims of the Ceaușescu regime.
On 26 June 2011, Elena and her second husband Alexander Nixon visited the Queen Elizabeth Sixth Form College in Darlington, County Durham, England to present awards to students who went to Romania for voluntary work and helping to build and repair housing in Brașov, a project based around the Roma community.
On 3 October 2011, Elena attended the 100th commemorative anniversary of the historic Western travels of ʻAbdu'l-Bahá in London, as a great-granddaughter of Queen Marie who had converted to the Baháʼí Faith, Elena spoke of how her great grandmother's Baháʼí legacy has inspired her to help those of need.
On 25 April 2012, for the Diamond Jubilee festivities of Queen Elizabeth II, Elena and her second husband inaugurated Royal teas: the UK's only Royal Tea room in Stanhope, County Durham.
Following the inauguration, on 19 May Elena along with King Michael I, Crown Princess Margareta, her brother-in-law Prince Radu, her husband Alexander Nixon and her son Prince Nicholas attended a Military parade at Windsor Great Park and a Garden party at Windsor Castle hosted by Prince Andrew, Duke of York and Prince Edward, Earl of Wessex.
Elena also annually attends the Guildhall banquet of the Guild of Freemen of the City of London and the delegation of the Two Sicilian Sacred Military Constantinian Order of Saint George in London.
In Romania

After 50 years of exile of the Romanian royal family from Romania, in 1990 Elena's sisters Crown Princess Margareta and Princess Sophie visited Romania for the first time following the Romanian Revolution and the overthrow of the Communist dictator Nicolae Ceaușescu in December 1989, she along with the royal family were involved in helping the Romanians.
Elena's first official appearance in Romania was on 19 April 1992 on Easter Day along with former King Michael I, his wife Anne, her first husband Robin Medforth-Mills, and her son Nicholas, where they were met with hundreds of thousands of supporters; Elena and her son Nicholas famously waved the Royal Flag from a balcony in Revolution Square.
She came again on Christmas Day of 1997 when the entire royal family entered Romania for the first time after 50 years of exile.
Since her first visit Elena occasionally visited Romania for family gatherings and for occasions such as: the 60th-birthday celebration of Crown Princess Margareta and the 90th-birthday celebrations of King Michael I.
However, since 2013 Elena has increased her activities in Romania by attending investiture ceremonies, presenting awards, book launches and Christmas gatherings.
Elena was present at the lying in state of King Michael
I in December 2017 and Queen Anne in August 2016 (held firstly at Peleș Castle, and then in the Throne Room of the Royal Palace in both cases), at their public funerals in Bucharest and at their burials in Curtea de Argeș.
Elena currently spends her time between Britain with her second husband Alexander and her daughter Elisabeta-Karina at her estate in Easington, County Durham and in Romania at Elisabeta Palace.
Marriages

First marriage

On 20 July 1983, Elena married Robin Medforth-Mills (1942–2002) in a civil ceremony at Durham, England.
The wedding party included King Michael I, his cousin former King Constantine II of Greece and his wife Queen Anne-Marie, who all served as Koumbaros; bridesmaids included her youngest sister Princess Maria, her second cousins Princess Alexia of Greece and Denmark and Princess Mafalda of Savoy; and also Fabiola Fruchaud, daughter of Princess Tatiana Radziwiłł.
Elena and Robin had two children:


They were divorced on 28 November 1991 after 8 years of marriage.
Second marriage

Elena was remarried on 14 August 1998 in a civil ceremony at Peterlee to Alexander Philips Nixon McAteer (born 22 October 1964).
Elena and Alexander married religiously at the Coronation Cathedral, Alba Iulia, on 11 September 2013, privately.



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
  AssignClass (a46d1700-b822-41ae-af2d-0502947db488)
 Call ID: a46d1700-b822-41ae-af2d-0502947db488
  Args:
    source: Princess Elena
    type: :Woman
  AssignClass (6dadc20b-e0b8-4a3b-839c-d31bf8bba19f)
 Call ID: 6dadc20b-e0b8-4a3b-839c-d31bf8bba19f
  Args:
    source: King Michael I
    type: :Man
  AssignClass (0910df4a-fc9d-4b25-b335-7a3faf66dda5)
 Call ID: 0910df4a-fc9d-4b25-b335-7a3faf66dda5
  Args:
    type: :Woman
    source: Queen Anne
  AddLiteral (0480441e-b769-4a51-aa60-5fc0f2465885)
 Call ID: 0480441e-b769-4a51-aa60-5fc0f2465885
  Args:
    source: Princess Elena
    literal_value: 1950
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddTriple (9e992350-4b69-4407-a3f3-aed008986b71)
 Call ID: 9e992350-4b69-4407-a3f3-aed008986b71
  Args:
    source: Princess Elena
    target: King Michael I
    relation: :hasFather
  AddTriple (8d72d5c7-9121-419a-b90a-c286951fd419)
 Call ID: 8d72d5c7-9121-419a-b90a-c286951fd419
  Args:
    relation: :hasMother
    source: Princess Elena
    target: Queen Anne
  AssignClass (854187a9-66a1-48df-82d0-76499ec9cb10)
 Call ID: 854187a9-66a1-48df-82d0-76499ec9cb10
  Args:
    source: Margareta
    type: :Woman
  AddTriple (ebf80bab-3bed-4f5f-9655-fa48055229e7)
 Call ID: ebf80bab-3bed-4f5f-9655-fa48055229e7
  Args:
    relation: :isSisterOf
    target: Margareta
    source: Princess Elena
  AssignClass (eb8197c8-eed6-44c9-a6fd-7c4f1cbb68f9)
 Call ID: eb8197c8-eed6-44c9-a6fd-7c4f1cbb68f9
  Args:
    source: Robin Medforth-Mills
    type: :Man
  AddLiteral (d00be219-e68a-45b2-bc4c-331d8e540cc4)
 Call ID: d00be219-e68a-45b2-bc4c-331d8e540cc4
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Robin Medforth-Mills
    literal_value: 1942
  AddLiteral (a92eeaa8-c6a2-4d44-bab9-526f03a6d766)
 Call ID: a92eeaa8-c6a2-4d44-bab9-526f03a6d766
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 2002
    source: Robin Medforth-Mills
  AddLiteral (89a1ccd4-ebb5-400b-a184-5a060389b42d)
 Call ID: 89a1ccd4-ebb5-400b-a184-5a060389b42d
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1983
    source: Princess Elena
  AssignClass (2ce4e8bc-0638-4b1a-ae4b-0349eb26e584)
 Call ID: 2ce4e8bc-0638-4b1a-ae4b-0349eb26e584
  Args:
    source: Prince Nicholas
    type: :Man
  AddTriple (5f738ef5-d6d0-4c72-9e99-d71401840f22)
 Call ID: 5f738ef5-d6d0-4c72-9e99-d71401840f22
  Args:
    target: Princess Elena
    source: Prince Nicholas
    relation: :isSonOf
  AddTriple (85652989-2029-45b8-bb48-628aeb0a1829)
 Call ID: 85652989-2029-45b8-bb48-628aeb0a1829
  Args:
    relation: :isSonOf
    source: Prince Nicholas
    target: Robin Medforth-Mills
  AssignClass (e615f9a3-d6e6-4831-9325-cb827b891ae0)
 Call ID: e615f9a3-d6e6-4831-9325-cb827b891ae0
  Args:
    source: Elisabeta-Karina
    type: :Woman
  AddTriple (f3ea201e-a72a-46b3-a564-dcddd74cb324)
 Call ID: f3ea201e-a72a-46b3-a564-dcddd74cb324
  Args:
    target: Princess Elena
    source: Elisabeta-Karina
    relation: :isDaughterOf
  AssignClass (536d0038-41b3-4100-9023-c705e290c5d3)
 Call ID: 536d0038-41b3-4100-9023-c705e290c5d3
  Args:
    type: :Man
    source: Alexander Nixon
  AddLiteral (24890c80-c9fc-4c75-ba89-9b7c7d1526d5)
 Call ID: 24890c80-c9fc-4c75-ba89-9b7c7d1526d5
  Args:
    literal_value: 1964
    source: Alexander Nixon
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (e632289c-354f-4832-8a06-9e5b17a29647)
 Call ID: e632289c-354f-4832-8a06-9e5b17a29647
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1998
    source: Princess Elena
  AssignClass (5ebae3ca-c8c2-478d-bed3-998745824441)
 Call ID: 5ebae3ca-c8c2-478d-bed3-998745824441
  Args:
    type: :Man
    source: Prince Radu
  AssignClass (419b57fb-fd94-441a-960b-6a95b3c7d97c)
 Call ID: 419b57fb-fd94-441a-960b-6a95b3c7d97c
  Args:
    type: :Woman
    source: Princess Irina
  AssignClass (ebf3b3c9-4966-4c7f-8cd1-93c0ccf5f146)
 Call ID: ebf3b3c9-4966-4c7f-8cd1-93c0ccf5f146
  Args:
    source: Princess Sophie
    type: :Woman
  AssignClass (1de705e4-b8ad-49b7-8529-a83f0a101eba)
 Call ID: 1de705e4-b8ad-49b7-8529-a83f0a101eba
  Args:
    source: Princess Maria
    type: :Woman
  AddTriple (ba0cccc5-82a2-4f3a-b5e9-048ed019b8cb)
 Call ID: ba0cccc5-82a2-4f3a-b5e9-048ed019b8cb
  Args:
    target: Princess Irina
    source: Princess Elena
    relation: :isSisterOf
  AddTriple (8f3af129-88df-445e-978f-b911040233f1)
 Call ID: 8f3af129-88df-445e-978f-b911040233f1
  Args:
    relation: :isSisterOf
    target: Princess Sophie
    source: Princess Elena
  AddTriple (2e89d93b-a804-4743-96a4-fa2fd2a29783)
 Call ID: 2e89d93b-a804-4743-96a4-fa2fd2a29783
  Args:
    source: Princess Elena
    target: Princess Maria
    relation: :isSisterOf
  Finish (e00d3fb2-159b-40e4-9e89-96644c89e8b1)
 Call ID: e00d3fb2-159b-40e4-9e89-96644c89e8b1
  Args: