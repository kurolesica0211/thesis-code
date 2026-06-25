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
Alfonso, Duke of Anjou, Duke of Cádiz, Grandee of Spain (Spanish: Don Alfonso Jaime Marcelino Manuel Víctor María de Borbón y Dampierre; French: Alphonse Jacques Marcellin Emmanuel Victor Marie de Bourbon; 20 April 1936 – 30 January 1989) was a grandson of King Alfonso XIII of Spain, a potential heir to the throne in the event of the restoration of the Spanish monarchy, and the Legitimist claimant to the throne of France.
Upbringing

Alfonso was born at Sant'Anna Clinic in Rome, the elder son of Infante Jaime, Duke of Segovia, King Alfonso's second of four sons.
His mother was Donna Emanuela de Dampierre, daughter of Roger, Duke of San Lorenzo and Donna Vittoria Ruspoli
The Segovias lived in Rome where Jaime's father had maintained a royal court-in-exile since the royal family fled Spain following the 1931 election of republicans and socialists in Spain's major cities.
Alfonso was baptised by Eugenio Cardinal Pacelli (later Pope Pius XII) at the Palazzo Ruspoli on the Via del Corso in Rome, home of his maternal grandmother, Donna Vittoria Ruspoli dei principi di Poggio Suasa.
In 1941, Alfonso and his parents followed his English-born grandmother, Queen Victoria Eugenie to Lausanne in Switzerland.
They lived first at the Hotel Royal, before Alfonso and his younger brother Gonzalo were sent to the Collège Saint-Jean (later Villa St. Jean International School) in Fribourg.
On 8 December 1946 Alfonso made his first communion with his brother, Gonzalo; on the same day he was confirmed by Pedro Cardinal Segura y Sáenz, Archbishop of Seville.
Spanish succession rights

The king's eldest son, Alfonso, Prince of Asturias, had inherited hemophilia from his maternal great-grandmother Queen Victoria, yet had been considered Spain's heir apparent until the republic was established in 1931.
Next in the line of succession, Infante Don Jaime, deaf and largely mute, was that same day persuaded to renounce his claim (and that of future descendants) alongside his elder brother, thereby assuming the Duke of Segovia title and clearing the way for King Alfonso's third son, Don Juan, Count of Barcelona to take up the monarchist cause on behalf of the banished dynasty.
There being no need for Segovia to contract a dynastic alliance, Emanuela de Dampierre's noble rather than royal background was looked upon approvingly by the former king and former queen when the couple wed in Rome in 1935, and neither style nor title is attributed to Alfonso de Borbón-Segovia y Dampierre in the 1944 edition of the Almanach de Gotha.
Following Alfonso XIII's death in Rome in February 1941, Franco wrote Don Juan, acknowledging him as rightful heir to the throne (though without inviting him to occupy it), implicitly confirming that he considered Segovia and his sons excluded from the royal succession.
The new law allowed Franco or his successor to choose any man "of royal lineage" as king, and Alfonso was mentioned that year as a possible alternative to Don Juan and his son, Juan Carlos, should Franco consider the former too liberal to reign over a Falangist Spain.
In December 1949, Segovia retracted his renunciation as coerced and claimed that he was the rightful claimant to Spain's crown.
Relations between Don Juan and Franco continued to deteriorate and in 1952 the latter prevailed upon Segovia to send his elder son to Spain to be educated under his guidance.
Reluctantly, Alfonso moved from Switzerland to Spain, initially to study law at Deusto University and, in 1955 to attend the elite Centro de Estudios Universitarios (CEU).
By 1956 Franco was diverting sponsors of some civic events from Juan Carlos, who was also being educated in Spain under the Caudillo's supervision, to Alfonso.
By 1964, Franco considered Juan Carlos his preferred candidate for the throne over his father, but also considered that if the latter deviated from obedience to Franco or loyalty to his Movimiento Nacional, Alfonso was a suitable alternative.
Alfonso's strongest supporter in Franco's government was José Solís Ruiz, minister and secretary-general of the Movimiento.
Anticipating that Franco would soon offer to declare him Spain's next king rather than Don Juan, in June 1969, Juan Carlos warned his father that if he declined Franco's offer, Alfonso would be invited to accept the crown, nevertheless Don Juan refused to consent to being bypassed.
Asked by Juan Carlos to be chief witness at the ceremony declaring him successor and Prince of Spain, Alfonso immediately agreed to do so and sent some of his supporters to visit his father in Paris to persuade him to express no opposition publicly.
In return for his full support, Franco later appointed Alfonso Spain's ambassador to Sweden.
But in June 1972, after he had taken up that post, Alfonso advised Franco's foreign minister Laureano López Rodó that he deemed his support conditional upon his cousin's continued loyalty to Francoist Spain.
He further hinted that Spain's law of succession should be amended to facilitate Alfonso's replacing or succeeding Juan Carlos as Franco's heir or on the throne, if circumstances called for such a change.
On 8 March 1972, in the Palace of El Pardo in Madrid, Alfonso married Doña María del Carmen Martínez-Bordiú y Franco, daughter of Don Cristóbal Martínez-Bordiú, 10th Marquis de Villaverde, and of his wife, Doña Carmen Franco y Polo (Franco's only daughter.
Doña Carmen was granted a title in 1975 becoming the 1st Duchess de Franco after Franco's death).
The witnesses of the marriage were Franco and Alfonso's mother.
Alfonso and Carmen separated in 1979, received a civil divorce in 1982 and an ecclesiastical annulment in 1986.
On 22 November 1972, General Franco awarded Alfonso the Spanish title Duque de Cádiz with the dignity Grandee of Spain, and he received the style of Royal Highness.
The Cádiz title had been held by Alfonso's great-great-grandfather, the Infante Francisco de Asís.
French succession rights

Since Alfonso's mother was not born a princess of royal descent, his grandfather Alfonso XIII did not consider young Alfonso in line to the Spanish throne in accordance with the Pragmatic Sanction of 1830.
Alfonso's father Jaime, however, came to assert that his sons were French dynasts entitled to the style of Royal Highness.
In Spain up until 1972, Alfonso was generally addressed as Don Alfonso de Borbón y Dampierre.
Elsewhere he was often addressed as a prince.
On 25 November 1950, Alfonso received the title Duc de Bourbon (Duke of Bourbon) from his father.
In 1963, Alfonso engaged the French historian and ardent royalist Hervé Pinoteau as his private secretary.
Pinoteau remained with him until the duke's death.
On 20 March 1975, Alfonso's father Jaime died.
On 3 August 1975, he took the courtesy title Duc d'Anjou (Duke of Anjou).
On 21 January 1985 (the 192nd anniversary of the death of King Louis XVI) Alfonso was present for the requiem mass at the Chapelle expiatoire in Paris.
Marriage and children

Lawsuit of the Count of Clermont against the Duke of Anjou

In 1987, his paternal 10th cousin Prince Henri of Orléans, Count of Clermont, eldest son of Henri, Count of Paris, the then Orléanist claimant to the defunct throne of France, initiated a court action against Alfonso for his use of the title Duke of Anjou and the coat-of-arms France Moderne (three fleur-de-lis or); Henri asked the court to fine Alfonso 50,000 French francs for each future violation.
In 1988, Prince Ferdinand, Duke of Castro and Prince Sixtus Henry of Bourbon-Parma joined Henri's lawsuit in reference to the use of the title Duke of Anjou, but not in respect to the coat-of-arms.
In 1989, Prince Henri d'Orléans and Prince Sixtus Henry of Bourbon-Parma appealed the judgment in the lawsuit about the use of a title and arms by Alfonso; the original judgment in favour of Alfonso was upheld.
Career

From 1977 to 1984, Alfonso was President of the Spanish Skiing Federation, and from 1984 to 1987 President of the Spanish Olympic Committee.
Death

Alfonso died in a skiing accident in Beaver Creek Resort, Eagle County, Colorado, on 30 January 1989, from broken neck by a cable which he collided with as it was being raised to support a banner at the finish line of a course at the FIS Alpine World Ski Championships.



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
  AssignClass (8b67425c-83ea-49a2-bb9c-45b30ba82b70)
 Call ID: 8b67425c-83ea-49a2-bb9c-45b30ba82b70
  Args:
    type: :Man
    source: Alfonso_Duke_of_Anjou
  AssignClass (74428a52-7a14-4c2c-9d11-0e8bda4badd2)
 Call ID: 74428a52-7a14-4c2c-9d11-0e8bda4badd2
  Args:
    type: :Person
    source: Alfonso_Duke_of_Anjou
  AddLiteral (045dd308-db11-4ca1-94a6-5c8df50c99af)
 Call ID: 045dd308-db11-4ca1-94a6-5c8df50c99af
  Args:
    literal_type: xsd:integer
    source: Alfonso_Duke_of_Anjou
    literal_value: 1936
    relation: :hasBirthYear
  AddLiteral (cb97917e-aa1a-4f19-8cc5-a696484e3606)
 Call ID: cb97917e-aa1a-4f19-8cc5-a696484e3606
  Args:
    relation: :hasDeathYear
    literal_value: 1989
    source: Alfonso_Duke_of_Anjou
    literal_type: xsd:integer
  AssignClass (94e99f38-d80a-42b6-8e79-0d5ee7473d0c)
 Call ID: 94e99f38-d80a-42b6-8e79-0d5ee7473d0c
  Args:
    source: Jaime_Duke_of_Segovia
    type: :Man
  AssignClass (ae85c099-88b8-4de0-8cae-3d968ba1db60)
 Call ID: ae85c099-88b8-4de0-8cae-3d968ba1db60
  Args:
    type: :Ancestor
    source: Jaime_Duke_of_Segovia
  AddTriple (d382b32c-89c8-4094-b70c-d794c211941d)
 Call ID: d382b32c-89c8-4094-b70c-d794c211941d
  Args:
    source: Alfonso_Duke_of_Anjou
    relation: :hasFather
    target: Jaime_Duke_of_Segovia
  AssignClass (6b4d9b6f-930f-43db-95a4-0175231f6a40)
 Call ID: 6b4d9b6f-930f-43db-95a4-0175231f6a40
  Args:
    source: Emanuela_de_Dampierre
    type: :Woman
  AssignClass (a1b227f9-d26e-4370-a938-8021e2f8bacc)
 Call ID: a1b227f9-d26e-4370-a938-8021e2f8bacc
  Args:
    type: :Ancestor
    source: Emanuela_de_Dampierre
  AddTriple (0a08be27-2d1b-4cb5-9513-a20db9cd9ced)
 Call ID: 0a08be27-2d1b-4cb5-9513-a20db9cd9ced
  Args:
    source: Alfonso_Duke_of_Anjou
    target: Emanuela_de_Dampierre
    relation: :hasMother
  AssignClass (902b23c1-1919-4288-8c6a-6abf9c48de32)
 Call ID: 902b23c1-1919-4288-8c6a-6abf9c48de32
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (d70955d1-89c1-4b6e-b3a8-332e06ff10ea)
 Call ID: d70955d1-89c1-4b6e-b3a8-332e06ff10ea
  Args:
    source: Alfonso_XIII_of_Spain
    type: :Ancestor
  AddTriple (0cf20034-766b-4eee-9539-271a34524249)
 Call ID: 0cf20034-766b-4eee-9539-271a34524249
  Args:
    source: Jaime_Duke_of_Segovia
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
  AssignClass (48e25142-9e41-4c5c-a69a-8a256897d265)
 Call ID: 48e25142-9e41-4c5c-a69a-8a256897d265
  Args:
    type: :Man
    source: Roger_Duke_of_San_Lorenzo
  AssignClass (a5d38401-c61a-4f01-93f8-9e69d17521e4)
 Call ID: a5d38401-c61a-4f01-93f8-9e69d17521e4
  Args:
    type: :Ancestor
    source: Roger_Duke_of_San_Lorenzo
  AddTriple (31bfd696-a42b-49f4-ae3c-83e22a91ce15)
 Call ID: 31bfd696-a42b-49f4-ae3c-83e22a91ce15
  Args:
    source: Emanuela_de_Dampierre
    target: Roger_Duke_of_San_Lorenzo
    relation: :hasFather
  AssignClass (cb5e72d0-d973-41a6-8a82-edc30d69d49b)
 Call ID: cb5e72d0-d973-41a6-8a82-edc30d69d49b
  Args:
    source: Vittoria_Ruspoli
    type: :Woman
  AssignClass (a64f4f31-6fa6-416e-9541-0c81b794ad85)
 Call ID: a64f4f31-6fa6-416e-9541-0c81b794ad85
  Args:
    type: :Ancestor
    source: Vittoria_Ruspoli
  AddTriple (312318f5-c623-4902-99da-2dca922f38cf)
 Call ID: 312318f5-c623-4902-99da-2dca922f38cf
  Args:
    source: Emanuela_de_Dampierre
    relation: :hasMother
    target: Vittoria_Ruspoli
  AssignClass (def63841-294f-4d8a-9e68-d8f5cbf6a434)
 Call ID: def63841-294f-4d8a-9e68-d8f5cbf6a434
  Args:
    type: :Man
    source: Gonzalo_de_Borbon
  AssignClass (a2f4888b-573d-4778-b661-cb860791c9b1)
 Call ID: a2f4888b-573d-4778-b661-cb860791c9b1
  Args:
    source: Gonzalo_de_Borbon
    type: :Person
  AddTriple (64bb6fbb-4cdc-40a6-82f4-4b0a278b7f56)
 Call ID: 64bb6fbb-4cdc-40a6-82f4-4b0a278b7f56
  Args:
    target: Gonzalo_de_Borbon
    relation: :hasBrother
    source: Alfonso_Duke_of_Anjou
  AddTriple (df2263d7-b79f-44a1-8a46-bd00766e3965)
 Call ID: df2263d7-b79f-44a1-8a46-bd00766e3965
  Args:
    relation: :hasFather
    target: Jaime_Duke_of_Segovia
    source: Gonzalo_de_Borbon
  AddTriple (78724576-edef-41e8-bd46-3eb14a52990d)
 Call ID: 78724576-edef-41e8-bd46-3eb14a52990d
  Args:
    relation: :hasMother
    target: Emanuela_de_Dampierre
    source: Gonzalo_de_Borbon
  AssignClass (3b74133e-6810-4cd2-b89a-fe754186d352)
 Call ID: 3b74133e-6810-4cd2-b89a-fe754186d352
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    type: :Woman
  AssignClass (06da3bfa-0517-4ab1-bb51-8e9ca920d0ff)
 Call ID: 06da3bfa-0517-4ab1-bb51-8e9ca920d0ff
  Args:
    type: :Person
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
  AddLiteral (00547aec-a423-4ccd-9cf7-88579ea0a9ab)
 Call ID: 00547aec-a423-4ccd-9cf7-88579ea0a9ab
  Args:
    relation: :hasMarriageYear
    literal_value: 1972
    source: Alfonso_Duke_of_Anjou
    literal_type: xsd:integer
  AddTriple (a43f5392-6145-4711-86f1-d69ac0eca590)
 Call ID: a43f5392-6145-4711-86f1-d69ac0eca590
  Args:
    relation: :hasRelation
    target: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    source: Alfonso_Duke_of_Anjou
  AssignClass (14197620-bf2a-4cde-8949-b0173de0eee0)
 Call ID: 14197620-bf2a-4cde-8949-b0173de0eee0
  Args:
    source: Cristobal_Martinez-Bordiu
    type: :Man
  AssignClass (01748523-409b-4d59-a22b-b4970c749207)
 Call ID: 01748523-409b-4d59-a22b-b4970c749207
  Args:
    source: Cristobal_Martinez-Bordiu
    type: :Ancestor
  AddTriple (1e43dd00-f02f-4352-83e5-3d84153babbe)
 Call ID: 1e43dd00-f02f-4352-83e5-3d84153babbe
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    relation: :hasFather
    target: Cristobal_Martinez-Bordiu
  AssignClass (31b049d9-a56f-4045-bd03-d1463b45c007)
 Call ID: 31b049d9-a56f-4045-bd03-d1463b45c007
  Args:
    type: :Woman
    source: Carmen_Franco_y_Polo
  AssignClass (6bc12a9d-6104-40ab-ae36-9d42616d160d)
 Call ID: 6bc12a9d-6104-40ab-ae36-9d42616d160d
  Args:
    type: :Ancestor
    source: Carmen_Franco_y_Polo
  AddTriple (4730104d-8884-4516-a04b-4fbbe6b4da99)
 Call ID: 4730104d-8884-4516-a04b-4fbbe6b4da99
  Args:
    source: Maria_del_Carmen_Martinez-Bordiu_y_Franco
    target: Carmen_Franco_y_Polo
    relation: :hasMother
  Finish (04678e61-80aa-4d04-95e6-789f0c93e130)
 Call ID: 04678e61-80aa-4d04-95e6-789f0c93e130
  Args: