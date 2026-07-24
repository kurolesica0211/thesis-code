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
  AssignClass (01469f92-2ec4-4e83-8a03-510d683e3971)
 Call ID: 01469f92-2ec4-4e83-8a03-510d683e3971
  Args:
    type: :Man
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (1340a809-6185-47f9-8468-cb9d839dedc1)
 Call ID: 1340a809-6185-47f9-8468-cb9d839dedc1
  Args:
    type: :Man
    source: Prince_Henry_Duke_of_Gloucester
  AssignClass (8a5623ff-764c-4402-a2aa-e5d07f32447e)
 Call ID: 8a5623ff-764c-4402-a2aa-e5d07f32447e
  Args:
    type: :Woman
    source: Princess_Alice_Duchess_of_Gloucester
  AddLiteral (38673f59-18d6-45ff-be3c-525d29962c4a)
 Call ID: 38673f59-18d6-45ff-be3c-525d29962c4a
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1944
    source: Prince_Richard_Duke_of_Gloucester
  AddTriple (d9f4effe-422c-417e-a488-4f008ca0cf0a)
 Call ID: d9f4effe-422c-417e-a488-4f008ca0cf0a
  Args:
    target: Prince_Henry_Duke_of_Gloucester
    source: Prince_Richard_Duke_of_Gloucester
    relation: :hasFather
  AddTriple (84159c92-2b57-4233-9835-71d7e70b7b09)
 Call ID: 84159c92-2b57-4233-9835-71d7e70b7b09
  Args:
    relation: :hasMother
    source: Prince_Richard_Duke_of_Gloucester
    target: Princess_Alice_Duchess_of_Gloucester
  AssignClass (39f2f73d-515b-468b-abbe-d8917c95dfde)
 Call ID: 39f2f73d-515b-468b-abbe-d8917c95dfde
  Args:
    type: :Man
    source: Prince_William_of_Gloucester
  AddTriple (9d763d0c-91de-45dc-878c-17cc508a937f)
 Call ID: 9d763d0c-91de-45dc-878c-17cc508a937f
  Args:
    relation: :hasBrother
    target: Prince_William_of_Gloucester
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (375d75f6-b086-47a3-b30e-4c24fdc954dd)
 Call ID: 375d75f6-b086-47a3-b30e-4c24fdc954dd
  Args:
    type: :Man
    source: King_George_V
  AssignClass (ead2301a-3d10-4978-b05c-67d3eea1f7d0)
 Call ID: ead2301a-3d10-4978-b05c-67d3eea1f7d0
  Args:
    type: :Woman
    source: Queen_Mary
  AddTriple (4645dafb-c135-46d1-bb15-4e84e359e804)
 Call ID: 4645dafb-c135-46d1-bb15-4e84e359e804
  Args:
    target: King_George_V
    source: Prince_Henry_Duke_of_Gloucester
    relation: :hasFather
  AddTriple (425d27e0-779a-4161-b2fa-ab39fdb5ed4c)
 Call ID: 425d27e0-779a-4161-b2fa-ab39fdb5ed4c
  Args:
    relation: :hasMother
    source: Prince_Henry_Duke_of_Gloucester
    target: Queen_Mary
  AssignClass (b20c8ed3-c3ff-4cf9-a709-33bd739027f6)
 Call ID: b20c8ed3-c3ff-4cf9-a709-33bd739027f6
  Args:
    type: :Man
    source: John_Montagu_Douglas_Scott_7th_Duke_of_Buccleuch
  AssignClass (1a291d5a-969c-472c-af81-76880e809418)
 Call ID: 1a291d5a-969c-472c-af81-76880e809418
  Args:
    type: :Woman
    source: Lady_Margaret_Bridgeman
  AddTriple (dde290ef-546a-43f9-9add-cf4395d1913e)
 Call ID: dde290ef-546a-43f9-9add-cf4395d1913e
  Args:
    relation: :hasFather
    target: John_Montagu_Douglas_Scott_7th_Duke_of_Buccleuch
    source: Princess_Alice_Duchess_of_Gloucester
  AddTriple (dae9ae5a-51fd-40e7-bc28-6380991e51f2)
 Call ID: dae9ae5a-51fd-40e7-bc28-6380991e51f2
  Args:
    source: Princess_Alice_Duchess_of_Gloucester
    target: Lady_Margaret_Bridgeman
    relation: :hasMother
  AssignClass (cc2320d2-e473-4dd1-9958-eb8fa410ad5c)
 Call ID: cc2320d2-e473-4dd1-9958-eb8fa410ad5c
  Args:
    type: :Woman
    source: Birgitte_van_Deurs_Henriksen
  AddLiteral (89e5ef30-518a-416b-bc9d-e150c532be06)
 Call ID: 89e5ef30-518a-416b-bc9d-e150c532be06
  Args:
    literal_value: 1972
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
    source: Prince_Richard_Duke_of_Gloucester
  AddTriple (c15287d3-6a97-4c67-af07-10dee92d23d3)
 Call ID: c15287d3-6a97-4c67-af07-10dee92d23d3
  Args:
    relation: :hasRelation
    source: Prince_Richard_Duke_of_Gloucester
    target: Birgitte_van_Deurs_Henriksen
  Finish (1f3ab9c3-4909-44a5-b5d3-d75ff1b674d2)
 Call ID: 1f3ab9c3-4909-44a5-b5d3-d75ff1b674d2
  Args: