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
Prince Richard, Duke of Gloucester (Richard Alexander Walter George; born 26 August 1944), is a member of the British royal family.
He is the second son of Prince Henry, Duke of Gloucester, and Princess Alice, Duchess of Gloucester, the youngest of the nine grandchildren of George V, nephew of Edward VIII and George VI, and first cousin of Elizabeth II.
He is 32nd in the line of succession to the British throne, and the highest person on the list who is not a descendant of George VI.
Richard practised as an architect until the death of his elder brother, William, placed him in direct line to inherit his father's dukedom of Gloucester, to which he succeeded in 1974.
Early life

Richard was born at 12:15 pm on 26 August 1944 at St Matthew's Nursing Home in Northampton, the second son of Prince Henry, Duke of Gloucester, and Alice, Duchess of Gloucester.
His father was the third son of King George V and Queen Mary.
His mother was the third daughter of John Montagu Douglas Scott, 7th Duke of Buccleuch, and Lady Margaret Bridgeman.
At the time of his birth, he was second in line to his father's dukedom, behind his elder brother, Prince William of Gloucester, who died in an air crash in 1972 before inheriting the title and having any children of his own.
Richard was baptised at the Royal Chapel of All Saints in Windsor Great Park on 20 October by the retired Archbishop of Canterbury, Cosmo Gordon Lang.
His godparents were his paternal aunt Princess Mary, Queen Elizabeth, Princess Marie Louise (his first cousin twice removed), Princess Alice, Countess of Athlone (his grandaunt and first cousin twice removed, for whom her daughter, Lady May Abel Smith stood proxy), the Duke of Buccleuch (his maternal uncle), the Marquess of Cambridge (his cousin), Lady Sybil Phipps (his maternal aunt), and General the Earl Alexander of Tunis (for whom his wife, then Lady Margaret Alexander, stood proxy).
When Richard was four months old, he accompanied his parents to Australia, where his father served as governor-general from 1945 to 1947.
The family returned to Barnwell Manor in 1947, where Richard spent most of his childhood.
Education and career

Richard's early education took place at home, under the instruction of Rosalind Ramirez, who had also tutored young King Faisal II of Iraq; later, he attended Wellesley House School at Broadstairs and Eton College.
In 1966, Richard joined the Offices Development Group in the Ministry of Public Building and Works for a year of practical work.
Marriage and family




On 8 July 1972, Richard married Danish-born Birgitte van Deurs Henriksen at St Andrew's Church, Barnwell, Northamptonshire; the Duke and Duchess of Gloucester have three children:


The Duke and Duchess of Gloucester's official residence is at Kensington Palace in London.
In September 2022, the Duke put the manor up for sale for £4.75 million.
Activities

Richard ended his architectural career in 1972, after the death of his elder brother Prince William, who was killed in an air crash during a flying competition.
Richard became heir apparent to his father's dukedom and had to take on additional family obligations and royal duties on behalf of the Queen.
He became Duke of Gloucester on his father's death on 10 June 1974.
He has been a corporate member of the Royal Institute of British Architects since 1972.
With his background in architecture, the Duke of Gloucester takes interest in the work of the trust and visits their projects, in addition to giving his name to their long standing Duke of Gloucester Young Achiever's Scheme Awards.
The Duke is vice president of Lepra, a UK-based leprosy charity; as part of this role, he attends national and international events in support of the charity's work.
He is royal patron of the Society of Antiquaries of London (and elected FSA) since 2001, royal patron of the UK branch of the charity Habitat for Humanity, royal patron of the St George's Society of New York, and president of The London Society.
A keen motorist, Richard passed the Advanced Driving Test of the Institute of Advanced Motorists, of which he was president for more than 32 years.
The Duke of Gloucester, accompanied by the Duchess, represented his cousin Elizabeth II at the Seychelles independence ceremonies on 26 June 1976 and again at the Solomon Islands independence celebrations on 7 July 1978.
He served as a judge in Prince Edward's charity television special The Grand Knockout Tournament on 15 June 1987.
On 10 April 2008, the Duke of Gloucester was officially installed as inaugural Chancellor of the University of Worcester during a ceremony at Worcester Cathedral.
The Duke carried out the first of these duties on 5 and 6 November 2008 at the Graduation Award Ceremonies.
The Duke is a patron of the Severn Valley Railway and the Pestalozzi International Village Trust.
He shares a name with an earlier Duke of Gloucester, Richard III, and has been patron of the Richard III Society since 1980.
He is a member of the international advisory board of the Royal United Services Institute.
During 2009, the Duke became patron of the de Havilland Aircraft Heritage Centre in support of its bid to raise funds through private means and through a bid for Heritage Lottery Funding.
In July 2011, the Duke visited the Isle of Man to meet with the representative of Manx National Heritage and the Council of Cancer Charities.
On 19 March 2013, the Duke represented Elizabeth II at the Vatican for the inauguration of Pope Francis.
On 11 March 2015, the Duke visited the Royal School Dungannon in County Tyrone to celebrate the 400th anniversary of the founding of the school; presenting a commemorative plaque and raising an anniversary flag on the grounds.
On 22 and 26 March 2015, the Duke represented the Queen at the ceremonies marking the reburial and commemorations of King Richard III in Leicester Cathedral.
Richard III had held the title Duke of Gloucester before his ascension to the English throne.
In March 2018, the Duke travelled to Malawi to attend the Commonwealth Day celebrations, and visited projects related to health services, wildlife, and climate change.
On 14 September 2022, after the death of Queen Elizabeth II on 8 September, the Duke joined her children, grandsons, nephew, and son-in-law, in walking in the state cortege from Buckingham Palace to Westminster Hall, for her lying in state.
In 2023 the Duke and Duchess of Gloucester attended the coronation of King Charles III and Queen Camilla in Westminster Abbey, and (in common with other working members of the royal family) took part in the Coronation Procession following the service.
Titles, styles, honours and arms

Titles and styles

Richard was originally styled "His Royal Highness Prince Richard of Gloucester".
Since becoming duke in 1974, he has been known as "His Royal Highness The Duke of Gloucester".
Honours

letters


Wear of orders, decorations, and medals

The ribbons worn regularly by Richard in undress uniform are as follows:


Honorary military appointments

Non-national titles and honours

Scholastic

Civic

Arms

Issue

Ancestry

See also

References

External links



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
  AssignClass (6ce4af44-1f12-43a0-97c2-1e0347e7485c)
 Call ID: 6ce4af44-1f12-43a0-97c2-1e0347e7485c
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    type: :Man
  AssignClass (b2c454a5-8b66-421d-86d2-874737d56d48)
 Call ID: b2c454a5-8b66-421d-86d2-874737d56d48
  Args:
    type: :Person
    source: Prince_Richard_Duke_of_Gloucester
  AddLiteral (8cf99b43-32f0-43ac-afe1-b714de055df0)
 Call ID: 8cf99b43-32f0-43ac-afe1-b714de055df0
  Args:
    literal_value: 1944
    source: Prince_Richard_Duke_of_Gloucester
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (465dd2d7-2a62-4163-935b-9b2b519f64c4)
 Call ID: 465dd2d7-2a62-4163-935b-9b2b519f64c4
  Args:
    source: Prince_Henry_Duke_of_Gloucester
    type: :Man
  AssignClass (d43061fb-7c89-4da6-99b2-caf154515da9)
 Call ID: d43061fb-7c89-4da6-99b2-caf154515da9
  Args:
    type: :Person
    source: Prince_Henry_Duke_of_Gloucester
  AssignClass (c047c51b-0ec7-40e7-adf9-54806fb4d792)
 Call ID: c047c51b-0ec7-40e7-adf9-54806fb4d792
  Args:
    source: Princess_Alice_Duchess_of_Gloucester
    type: :Woman
  AssignClass (08f47a7e-ab83-45bb-9cc7-c64cafb280fa)
 Call ID: 08f47a7e-ab83-45bb-9cc7-c64cafb280fa
  Args:
    source: Princess_Alice_Duchess_of_Gloucester
    type: :Person
  AddTriple (243d2f87-7574-448b-9e75-cb7e647dac23)
 Call ID: 243d2f87-7574-448b-9e75-cb7e647dac23
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    target: Prince_Henry_Duke_of_Gloucester
    relation: :hasFather
  AddTriple (a9fa05ea-c0a7-4b3b-969c-7caccdd2b0c2)
 Call ID: a9fa05ea-c0a7-4b3b-969c-7caccdd2b0c2
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    relation: :hasMother
    target: Princess_Alice_Duchess_of_Gloucester
  AssignClass (eed6c05c-a2bc-4d93-9925-bed15e035abf)
 Call ID: eed6c05c-a2bc-4d93-9925-bed15e035abf
  Args:
    type: :Man
    source: George_V
  AssignClass (e6b045bf-affe-4097-a272-d25d0ea1db92)
 Call ID: e6b045bf-affe-4097-a272-d25d0ea1db92
  Args:
    source: George_V
    type: :Person
  AssignClass (3bc1df4a-378a-42b3-9a62-ecb8d6636aa1)
 Call ID: 3bc1df4a-378a-42b3-9a62-ecb8d6636aa1
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (38af3653-225c-40db-b6b5-282de51c637f)
 Call ID: 38af3653-225c-40db-b6b5-282de51c637f
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (46e0cf4c-d9af-4701-95cd-db9dd4a91d17)
 Call ID: 46e0cf4c-d9af-4701-95cd-db9dd4a91d17
  Args:
    relation: :hasFather
    target: George_V
    source: Prince_Henry_Duke_of_Gloucester
  AddTriple (1b728b08-71aa-48d0-9bbb-828cb28f73a5)
 Call ID: 1b728b08-71aa-48d0-9bbb-828cb28f73a5
  Args:
    relation: :hasMother
    target: Queen_Mary
    source: Prince_Henry_Duke_of_Gloucester
  AssignClass (4402f49c-17bd-4cc3-b0f1-8d1268c9e1ed)
 Call ID: 4402f49c-17bd-4cc3-b0f1-8d1268c9e1ed
  Args:
    source: Prince_William_of_Gloucester
    type: :Man
  AssignClass (c12b0ecb-d887-4c3d-b652-76cc24e23391)
 Call ID: c12b0ecb-d887-4c3d-b652-76cc24e23391
  Args:
    type: :Person
    source: Prince_William_of_Gloucester
  AddTriple (a49ecf5a-1f55-498b-9707-0443e5a1baab)
 Call ID: a49ecf5a-1f55-498b-9707-0443e5a1baab
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    relation: :isBrotherOf
    target: Prince_William_of_Gloucester
  AddTriple (ad6e6f43-198d-46a8-9bf2-d630b56dc613)
 Call ID: ad6e6f43-198d-46a8-9bf2-d630b56dc613
  Args:
    source: Prince_William_of_Gloucester
    relation: :hasFather
    target: Prince_Henry_Duke_of_Gloucester
  AddTriple (70d7c69a-1dee-4d8f-a3eb-39efd1b05365)
 Call ID: 70d7c69a-1dee-4d8f-a3eb-39efd1b05365
  Args:
    target: Princess_Alice_Duchess_of_Gloucester
    relation: :hasMother
    source: Prince_William_of_Gloucester
  AddLiteral (7788db68-24b9-4e62-9cd9-57073ede2be9)
 Call ID: 7788db68-24b9-4e62-9cd9-57073ede2be9
  Args:
    source: Prince_William_of_Gloucester
    literal_value: 1972
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (f3e4a403-7b29-470a-a796-38e9237bf268)
 Call ID: f3e4a403-7b29-470a-a796-38e9237bf268
  Args:
    type: :Man
    source: John_Montagu_Douglas_Scott_7th_Duke_of_Buccleuch
  AssignClass (fc33bf30-24cb-4932-97a3-94a06f3531d1)
 Call ID: fc33bf30-24cb-4932-97a3-94a06f3531d1
  Args:
    type: :Person
    source: John_Montagu_Douglas_Scott_7th_Duke_of_Buccleuch
  AssignClass (44d65a87-ce49-4cbf-b406-32d0a898bc00)
 Call ID: 44d65a87-ce49-4cbf-b406-32d0a898bc00
  Args:
    source: Lady_Margaret_Bridgeman
    type: :Woman
  AssignClass (b1d53270-1f8f-4571-8ca1-7bcb808437d2)
 Call ID: b1d53270-1f8f-4571-8ca1-7bcb808437d2
  Args:
    source: Lady_Margaret_Bridgeman
    type: :Person
  AddTriple (cb887b8a-868e-4f4f-89f1-8285f492decb)
 Call ID: cb887b8a-868e-4f4f-89f1-8285f492decb
  Args:
    source: Princess_Alice_Duchess_of_Gloucester
    relation: :hasFather
    target: John_Montagu_Douglas_Scott_7th_Duke_of_Buccleuch
  AddTriple (d52be7e9-8793-48fa-a98c-71483a4cf091)
 Call ID: d52be7e9-8793-48fa-a98c-71483a4cf091
  Args:
    relation: :hasMother
    target: Lady_Margaret_Bridgeman
    source: Princess_Alice_Duchess_of_Gloucester
  AssignClass (ac949736-93dd-4d0e-96ec-0bf687980f54)
 Call ID: ac949736-93dd-4d0e-96ec-0bf687980f54
  Args:
    source: Birgitte_van_Deurs_Henriksen
    type: :Woman
  AssignClass (f6d74f85-e84f-49ba-b8aa-d19670655e75)
 Call ID: f6d74f85-e84f-49ba-b8aa-d19670655e75
  Args:
    source: Birgitte_van_Deurs_Henriksen
    type: :Person
  AddTriple (3c81fdee-2b87-405a-86a1-9c3e26a4839e)
 Call ID: 3c81fdee-2b87-405a-86a1-9c3e26a4839e
  Args:
    relation: :hasRelation
    target: Birgitte_van_Deurs_Henriksen
    source: Prince_Richard_Duke_of_Gloucester
  AddLiteral (9616f176-ebaf-4713-b2f0-0dcc89ba736c)
 Call ID: 9616f176-ebaf-4713-b2f0-0dcc89ba736c
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1972
    source: Prince_Richard_Duke_of_Gloucester
  Finish (4ffa159a-8883-43c9-9a97-2b3b89ca7264)
 Call ID: 4ffa159a-8883-43c9-9a97-2b3b89ca7264
  Args: