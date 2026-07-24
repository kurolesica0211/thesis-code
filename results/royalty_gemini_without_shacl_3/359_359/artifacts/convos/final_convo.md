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
  AssignClass (0c27ea33-e042-4c59-9408-59ef4c45b876)
 Call ID: 0c27ea33-e042-4c59-9408-59ef4c45b876
  Args:
    type: :Man
    source: Alfonso_Duke_of_Anjou
  AssignClass (dacbad6e-e881-4be1-ba04-928bb646788f)
 Call ID: dacbad6e-e881-4be1-ba04-928bb646788f
  Args:
    type: :Person
    source: Alfonso_Duke_of_Anjou
  AddLiteral (bdc5f46d-dd7c-4408-84f1-790534589196)
 Call ID: bdc5f46d-dd7c-4408-84f1-790534589196
  Args:
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasBirthYear
    source: Alfonso_Duke_of_Anjou
  AddLiteral (5c3e58ea-c6af-41f7-8e05-3daae859bc54)
 Call ID: 5c3e58ea-c6af-41f7-8e05-3daae859bc54
  Args:
    literal_type: xsd:integer
    source: Alfonso_Duke_of_Anjou
    literal_value: 1989
    relation: :hasDeathYear
  AssignClass (3599411a-8436-492e-a5c9-094d7c20b2ae)
 Call ID: 3599411a-8436-492e-a5c9-094d7c20b2ae
  Args:
    type: :Man
    source: Jaime_Duke_of_Segovia
  AssignClass (a5f84641-f600-4c25-bff8-e32b89ab4812)
 Call ID: a5f84641-f600-4c25-bff8-e32b89ab4812
  Args:
    type: :Person
    source: Jaime_Duke_of_Segovia
  AddTriple (609667f0-38ed-425f-987f-53f3d497d4da)
 Call ID: 609667f0-38ed-425f-987f-53f3d497d4da
  Args:
    source: Alfonso_Duke_of_Anjou
    relation: :hasFather
    target: Jaime_Duke_of_Segovia
  AssignClass (5f93c141-856b-4e41-bb2b-712c923bcf37)
 Call ID: 5f93c141-856b-4e41-bb2b-712c923bcf37
  Args:
    type: :Woman
    source: Emanuela_de_Dampierre
  AssignClass (5f0de6db-cb63-4cae-a58e-968dba8a5333)
 Call ID: 5f0de6db-cb63-4cae-a58e-968dba8a5333
  Args:
    type: :Person
    source: Emanuela_de_Dampierre
  AddTriple (d46ea4a8-30fa-40f4-8cc2-13bd44a1f7fe)
 Call ID: d46ea4a8-30fa-40f4-8cc2-13bd44a1f7fe
  Args:
    target: Emanuela_de_Dampierre
    relation: :hasMother
    source: Alfonso_Duke_of_Anjou
  AssignClass (0bf0e249-3e34-463f-be6c-108ec45024b7)
 Call ID: 0bf0e249-3e34-463f-be6c-108ec45024b7
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (be67f95a-0479-4036-9ea1-f8b5ab40334f)
 Call ID: be67f95a-0479-4036-9ea1-f8b5ab40334f
  Args:
    type: :Person
    source: Alfonso_XIII_of_Spain
  AddTriple (ead51110-e372-44b6-9144-50741c3a9298)
 Call ID: ead51110-e372-44b6-9144-50741c3a9298
  Args:
    source: Jaime_Duke_of_Segovia
    relation: :hasFather
    target: Alfonso_XIII_of_Spain
  AssignClass (4fc0cf02-d5fb-4541-9b06-a3e66526a962)
 Call ID: 4fc0cf02-d5fb-4541-9b06-a3e66526a962
  Args:
    type: :Man
    source: Roger_Duke_of_San_Lorenzo
  AssignClass (b4aef1d2-98ff-44ac-85e2-3fc19848d9db)
 Call ID: b4aef1d2-98ff-44ac-85e2-3fc19848d9db
  Args:
    type: :Person
    source: Roger_Duke_of_San_Lorenzo
  AssignClass (c7f90de6-56b4-4468-9efc-44a501051606)
 Call ID: c7f90de6-56b4-4468-9efc-44a501051606
  Args:
    type: :Woman
    source: Vittoria_Ruspoli
  AssignClass (f702c8d2-0b4b-4842-a98e-30472a665275)
 Call ID: f702c8d2-0b4b-4842-a98e-30472a665275
  Args:
    type: :Person
    source: Vittoria_Ruspoli
  AddTriple (4029bb6f-e846-4b58-ac31-8391207e7949)
 Call ID: 4029bb6f-e846-4b58-ac31-8391207e7949
  Args:
    target: Roger_Duke_of_San_Lorenzo
    relation: :hasFather
    source: Emanuela_de_Dampierre
  AddTriple (83d1087f-d1be-443a-a112-6352f519bd35)
 Call ID: 83d1087f-d1be-443a-a112-6352f519bd35
  Args:
    target: Vittoria_Ruspoli
    source: Emanuela_de_Dampierre
    relation: :hasMother
  AssignClass (59b6dcd6-013d-46d3-a742-c32f5d030bdc)
 Call ID: 59b6dcd6-013d-46d3-a742-c32f5d030bdc
  Args:
    type: :Man
    source: Gonzalo
  AssignClass (febe04fb-b81c-4fb8-988a-ac3c78cc252f)
 Call ID: febe04fb-b81c-4fb8-988a-ac3c78cc252f
  Args:
    type: :Person
    source: Gonzalo
  AddTriple (6bbb0f36-849e-4f2f-b7f3-c282a934261e)
 Call ID: 6bbb0f36-849e-4f2f-b7f3-c282a934261e
  Args:
    relation: :isSiblingOf
    source: Alfonso_Duke_of_Anjou
    target: Gonzalo
  AssignClass (81667245-193b-4968-a970-29d4738fa562)
 Call ID: 81667245-193b-4968-a970-29d4738fa562
  Args:
    type: :Woman
    source: Victoria_Eugenie
  AssignClass (cf523618-7847-48b2-977d-dace9fed7849)
 Call ID: cf523618-7847-48b2-977d-dace9fed7849
  Args:
    type: :Person
    source: Victoria_Eugenie
  AssignClass (124e1523-1642-406f-b203-86d77b84fddb)
 Call ID: 124e1523-1642-406f-b203-86d77b84fddb
  Args:
    type: :Woman
    source: Maria_del_Carmen_Martinez_Bordiu_y_Franco
  AssignClass (d139dc4c-7bee-4dde-b1cd-f32aaacd49d2)
 Call ID: d139dc4c-7bee-4dde-b1cd-f32aaacd49d2
  Args:
    type: :Person
    source: Maria_del_Carmen_Martinez_Bordiu_y_Franco
  AddTriple (ab008bbb-287c-43b9-9716-2792fc37fb06)
 Call ID: ab008bbb-287c-43b9-9716-2792fc37fb06
  Args:
    target: Maria_del_Carmen_Martinez_Bordiu_y_Franco
    relation: :hasRelation
    source: Alfonso_Duke_of_Anjou
  AddLiteral (1d0836e6-95e7-4f21-98c6-5856d35f5c9a)
 Call ID: 1d0836e6-95e7-4f21-98c6-5856d35f5c9a
  Args:
    literal_value: 1972
    relation: :hasMarriageYear
    source: Alfonso_Duke_of_Anjou
    literal_type: xsd:integer
  AssignClass (15ea558d-a4a0-4058-9e21-15ad1cf63666)
 Call ID: 15ea558d-a4a0-4058-9e21-15ad1cf63666
  Args:
    type: :Man
    source: Cristobal_Martinez_Bordiu
  AssignClass (e7001377-95a9-402f-a6c7-4b65eb66c752)
 Call ID: e7001377-95a9-402f-a6c7-4b65eb66c752
  Args:
    type: :Person
    source: Cristobal_Martinez_Bordiu
  AssignClass (c5aecca5-9cb5-408b-ac2e-2e43a63dc133)
 Call ID: c5aecca5-9cb5-408b-ac2e-2e43a63dc133
  Args:
    type: :Woman
    source: Carmen_Franco_y_Polo
  AssignClass (733a8894-38db-49c6-9c87-ab3550438534)
 Call ID: 733a8894-38db-49c6-9c87-ab3550438534
  Args:
    type: :Person
    source: Carmen_Franco_y_Polo
  AddTriple (66102af4-5eec-4e3e-bf38-22b6b331742f)
 Call ID: 66102af4-5eec-4e3e-bf38-22b6b331742f
  Args:
    target: Cristobal_Martinez_Bordiu
    source: Maria_del_Carmen_Martinez_Bordiu_y_Franco
    relation: :hasFather
  AddTriple (84fc4d9f-4261-446e-a9e2-f844ce3d9aed)
 Call ID: 84fc4d9f-4261-446e-a9e2-f844ce3d9aed
  Args:
    target: Carmen_Franco_y_Polo
    source: Maria_del_Carmen_Martinez_Bordiu_y_Franco
    relation: :hasMother
  AssignClass (b0b29bec-8d86-40a3-8e3d-b283048be069)
 Call ID: b0b29bec-8d86-40a3-8e3d-b283048be069
  Args:
    type: :Man
    source: Juan_Carlos_I_of_Spain
  AssignClass (1540d10f-bb4f-41e8-a2da-d1e23c5aedb5)
 Call ID: 1540d10f-bb4f-41e8-a2da-d1e23c5aedb5
  Args:
    type: :Person
    source: Juan_Carlos_I_of_Spain
  AddTriple (7a62c3ab-1c32-4c2f-a170-4c17980debba)
 Call ID: 7a62c3ab-1c32-4c2f-a170-4c17980debba
  Args:
    target: Juan_Carlos_I_of_Spain
    relation: :isSiblingOf
    source: Alfonso_Duke_of_Anjou
  Finish (d7e52346-9fcd-4016-b569-8351594a5820)
 Call ID: d7e52346-9fcd-4016-b569-8351594a5820
  Args: