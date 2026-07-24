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
  AssignClass (cd78c575-e8d2-48d0-9b48-fed0ee598de8)
 Call ID: cd78c575-e8d2-48d0-9b48-fed0ee598de8
  Args:
    type: :Woman
    source: Princess_Elena
  AssignClass (8d4a699d-d10f-4145-a1a7-09d6719d6af1)
 Call ID: 8d4a699d-d10f-4145-a1a7-09d6719d6af1
  Args:
    type: :Person
    source: Princess_Elena
  AddLiteral (555c533a-04d1-41ff-82e7-bbc516184d15)
 Call ID: 555c533a-04d1-41ff-82e7-bbc516184d15
  Args:
    literal_type: xsd:integer
    source: Princess_Elena
    relation: :hasBirthYear
    literal_value: 1950
  AssignClass (43c32b9b-9f0a-4a52-945c-3882cdd125c2)
 Call ID: 43c32b9b-9f0a-4a52-945c-3882cdd125c2
  Args:
    type: :Man
    source: King_Michael_I
  AssignClass (4b79f780-9102-4d95-8b16-78b21fff63f2)
 Call ID: 4b79f780-9102-4d95-8b16-78b21fff63f2
  Args:
    type: :Person
    source: King_Michael_I
  AssignClass (8a5d7f79-d4a1-44ce-94f5-010190957ad7)
 Call ID: 8a5d7f79-d4a1-44ce-94f5-010190957ad7
  Args:
    type: :Woman
    source: Queen_Anne
  AssignClass (f2a089fb-ddb0-4911-90b2-a4acc8d39da8)
 Call ID: f2a089fb-ddb0-4911-90b2-a4acc8d39da8
  Args:
    type: :Person
    source: Queen_Anne
  AddTriple (9f0d5785-b68d-4b52-b5c8-4c5a3a8be04d)
 Call ID: 9f0d5785-b68d-4b52-b5c8-4c5a3a8be04d
  Args:
    relation: :isDaughterOf
    source: Princess_Elena
    target: King_Michael_I
  AddTriple (7d991e35-ed0a-40c5-b874-e20edb165cd8)
 Call ID: 7d991e35-ed0a-40c5-b874-e20edb165cd8
  Args:
    source: Princess_Elena
    target: Queen_Anne
    relation: :isDaughterOf
  AssignClass (9e3fdfd3-443f-4109-b7cb-fa5cd62cc14a)
 Call ID: 9e3fdfd3-443f-4109-b7cb-fa5cd62cc14a
  Args:
    type: :Woman
    source: Crown_Princess_Margareta
  AssignClass (0ba48ce5-278e-4cf1-89d6-35569ef63b33)
 Call ID: 0ba48ce5-278e-4cf1-89d6-35569ef63b33
  Args:
    type: :Person
    source: Crown_Princess_Margareta
  AddTriple (7c98f8ff-1fa4-4717-a2c7-1addde60d5e3)
 Call ID: 7c98f8ff-1fa4-4717-a2c7-1addde60d5e3
  Args:
    target: Crown_Princess_Margareta
    source: Princess_Elena
    relation: :isSisterOf
  AssignClass (04cef476-fd11-406e-a1e2-8a24f66d5f74)
 Call ID: 04cef476-fd11-406e-a1e2-8a24f66d5f74
  Args:
    type: :Man
    source: Prince_Radu
  AssignClass (633388a9-81b1-497a-8f4d-e8eb3608122b)
 Call ID: 633388a9-81b1-497a-8f4d-e8eb3608122b
  Args:
    type: :Person
    source: Prince_Radu
  AddTriple (62beb32d-0813-4ae8-ba83-4e65bedcf51c)
 Call ID: 62beb32d-0813-4ae8-ba83-4e65bedcf51c
  Args:
    relation: :isSisterOf
    source: Princess_Elena
    target: Prince_Radu
  AssignClass (eacbdbc1-a34f-439c-902f-dcbbd78585d7)
 Call ID: eacbdbc1-a34f-439c-902f-dcbbd78585d7
  Args:
    type: :Man
    source: Robin_Medforth-Mills
  AssignClass (ede47c41-3a27-426c-b946-461bde0f430b)
 Call ID: ede47c41-3a27-426c-b946-461bde0f430b
  Args:
    type: :Person
    source: Robin_Medforth-Mills
  AddLiteral (1a2a2b69-415c-4e3a-9b5c-42065e9100e4)
 Call ID: 1a2a2b69-415c-4e3a-9b5c-42065e9100e4
  Args:
    literal_type: xsd:integer
    source: Princess_Elena
    relation: :hasMarriageYear
    literal_value: 1983
  AddTriple (712bc756-a7ca-4d7a-935a-b5584ca4ffc5)
 Call ID: 712bc756-a7ca-4d7a-935a-b5584ca4ffc5
  Args:
    target: Robin_Medforth-Mills
    source: Princess_Elena
    relation: :hasRelation
  AssignClass (a6fc474a-5f70-4542-8280-639c929512d1)
 Call ID: a6fc474a-5f70-4542-8280-639c929512d1
  Args:
    type: :Man
    source: Prince_Nicholas
  AssignClass (5dddfb60-ebe9-42b4-b049-0e0f43a82e1a)
 Call ID: 5dddfb60-ebe9-42b4-b049-0e0f43a82e1a
  Args:
    type: :Person
    source: Prince_Nicholas
  AddTriple (469b37ce-ac85-4cf2-a329-6e83879cefa8)
 Call ID: 469b37ce-ac85-4cf2-a329-6e83879cefa8
  Args:
    relation: :isSonOf
    target: Princess_Elena
    source: Prince_Nicholas
  AddTriple (442fc4ec-9430-423f-a645-9f90db612c35)
 Call ID: 442fc4ec-9430-423f-a645-9f90db612c35
  Args:
    relation: :isSonOf
    source: Prince_Nicholas
    target: Robin_Medforth-Mills
  AssignClass (00f75610-fcff-4250-8f11-5f1187263963)
 Call ID: 00f75610-fcff-4250-8f11-5f1187263963
  Args:
    type: :Man
    source: Alexander_Nixon
  AssignClass (cfcd4cd5-073d-4abd-90bf-9120b26e01ab)
 Call ID: cfcd4cd5-073d-4abd-90bf-9120b26e01ab
  Args:
    type: :Person
    source: Alexander_Nixon
  AddLiteral (5342e5da-dc4b-43a4-af4b-bdc3bd846a1a)
 Call ID: 5342e5da-dc4b-43a4-af4b-bdc3bd846a1a
  Args:
    literal_type: xsd:integer
    source: Princess_Elena
    relation: :hasMarriageYear
    literal_value: 1998
  AddTriple (5d7aa0ca-3a93-4f1b-98ad-c5f778e528b3)
 Call ID: 5d7aa0ca-3a93-4f1b-98ad-c5f778e528b3
  Args:
    source: Princess_Elena
    target: Alexander_Nixon
    relation: :hasRelation
  AssignClass (20f960ea-e50c-4807-aadc-a43704a398ff)
 Call ID: 20f960ea-e50c-4807-aadc-a43704a398ff
  Args:
    type: :Woman
    source: Elisabeta-Karina
  AssignClass (e21b579d-d1dc-4bbf-9dff-c725b145184a)
 Call ID: e21b579d-d1dc-4bbf-9dff-c725b145184a
  Args:
    type: :Person
    source: Elisabeta-Karina
  AddTriple (1d09b20e-70d6-4579-93ac-2dee37942078)
 Call ID: 1d09b20e-70d6-4579-93ac-2dee37942078
  Args:
    relation: :isDaughterOf
    target: Princess_Elena
    source: Elisabeta-Karina
  AddTriple (f515be29-b99b-4b09-825f-f7044a6e6d04)
 Call ID: f515be29-b99b-4b09-825f-f7044a6e6d04
  Args:
    relation: :isDaughterOf
    source: Elisabeta-Karina
    target: Alexander_Nixon
  AssignClass (5e49db31-de52-4f2f-aed0-adf47ff718ef)
 Call ID: 5e49db31-de52-4f2f-aed0-adf47ff718ef
  Args:
    type: :Woman
    source: Princess_Irina
  AssignClass (cfc1ce21-6f0e-4c38-be0c-132b2e2c543c)
 Call ID: cfc1ce21-6f0e-4c38-be0c-132b2e2c543c
  Args:
    type: :Person
    source: Princess_Irina
  AssignClass (218f37c2-55a5-4b7a-a5ee-bacf405ec29c)
 Call ID: 218f37c2-55a5-4b7a-a5ee-bacf405ec29c
  Args:
    type: :Woman
    source: Princess_Sophie
  AssignClass (af5c9c11-88a3-4ae3-83a5-50b235dba47f)
 Call ID: af5c9c11-88a3-4ae3-83a5-50b235dba47f
  Args:
    type: :Person
    source: Princess_Sophie
  AssignClass (081bbc7a-f686-40b4-9fdd-d35b80ca3670)
 Call ID: 081bbc7a-f686-40b4-9fdd-d35b80ca3670
  Args:
    type: :Woman
    source: Princess_Maria
  AssignClass (e57820b6-4899-4a6b-b21f-1d93eb7d7099)
 Call ID: e57820b6-4899-4a6b-b21f-1d93eb7d7099
  Args:
    type: :Person
    source: Princess_Maria
  AddTriple (0743b0c5-e051-419b-b450-8a1bc8f08531)
 Call ID: 0743b0c5-e051-419b-b450-8a1bc8f08531
  Args:
    relation: :isSisterOf
    source: Princess_Elena
    target: Princess_Irina
  AddTriple (90ff4a1d-d771-4d39-aae1-97ee34821167)
 Call ID: 90ff4a1d-d771-4d39-aae1-97ee34821167
  Args:
    relation: :isSisterOf
    source: Princess_Elena
    target: Princess_Sophie
  AddTriple (8b3c01d8-f52e-40a3-aa65-c772fd467157)
 Call ID: 8b3c01d8-f52e-40a3-aa65-c772fd467157
  Args:
    relation: :isSisterOf
    target: Princess_Maria
    source: Princess_Elena
  Finish (3e708592-512a-4c63-ab68-28d734d0a3ad)
 Call ID: 3e708592-512a-4c63-ab68-28d734d0a3ad
  Args: