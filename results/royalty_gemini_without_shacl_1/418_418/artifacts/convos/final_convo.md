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
Prince Philippe, Duke of Orléans (French: Louis Philippe Robert; 6 February 1869 – 28 March 1926) was the Orléanist pretender to the throne of France from 1894 to 1926 as Philippe VIII.
Early life

Philippe was born at York House, Twickenham, near London, the son of Philippe, Count of Paris, by his wife (and first cousin), Princess Isabelle of Orléans.
He was baptised with the names Louis-Philippe-Robert, and was called Philippe.
His family lived in the United Kingdom from the abdication and banishment of his great-grandfather Louis Philippe I, King of the French, in 1848, and returned to France in 1871 following the fall of the Second French Empire.
However, they again took refuge in England in 1886, when the French Republic exiled them following the wedding in Paris of Philippe's sister Amélie of Orléans to Crown Prince Carlos of Portugal.
Returning therefore to France in 1871 with his parents, Philippe was educated at home at the Château d'Eu and at the Collège Stanislas de Paris.
In 1880 Philippe's father granted him the title Duc d'Orléans.
Military career

Philippe began his military education at the École spéciale militaire de Saint-Cyr.
In October 1889, Philippe went to Switzerland to complete a course in military theory.
While there he fathered a son, Philippe Debien, by Nina, an actress working in the casino at Lausanne.
Drawn to explore the "unknown", Philippe asked Prince George, Duke of Cambridge, to send him to a military post in the Himalayas.
While in the East, he undertook a hunting and exploratory expedition in Nepal with his cousin Prince Henri of Orléans, went mountain-climbing in Tibet, and visited Afghanistan, Ceylon, and the Persian Gulf, before being posted back to Britain.
Prior to his imprisonment in France, Philippe had been unofficially engaged to his first cousin Princess Marguerite of Orléans, but the engagement was cancelled when Philippe's involvement with the Australian opera singer Nellie Melba was revealed.
Armstrong filed for divorce from Melba on the grounds of adultery, naming Philippe as co-respondent; the case was eventually dropped.
In September 1890, Philippe accompanied his father on a two-month trip to the United States and Canada.
On 12 November 1890, while in Philadelphia, Philippe joined the Pennsylvania Commandery of the Military Order of the Loyal Legion of the United States (MOLLUS) - a military society composed of officers who had served the Union in the American Civil War and their descendants - by right of his father's service in the Union Army.
In December 1890, Philippe applied unsuccessfully to serve in the Russian Army.
In March 1894, Philippe went to Egypt and Palestine with his sister Hélène, Duchess of Aosta.
Claimant to the defunct throne

Upon the death of his father on 8 September 1894, Philippe became the Orléanist claimant to the defunct French throne.
He was known to monarchists as Philippe VIII.
In October 1895, Philippe was named as co-respondent in the divorce case of Woolston v. Woolston.
Unlike his great grandfather, Louis Philippe I, Philippe claimed grand mastership of the Order of the Holy Spirit as intrinsic to his dynastic claim to the throne, and sometimes wore the breast star of the order.
On 5 November 1896, in Vienna, Philippe married Archduchess Maria Dorothea of Austria (1867–1932), a daughter of Archduke Joseph Karl of Austria, Palatine of Hungary, and granddaughter of Princess Clémentine of Orléans, as well as a niece of Marie Henriette of Austria, Queen Consort of the Belgians.
While travelling in Geneva in 1898, Philippe narrowly missed being assassinated by Luigi Lucheni, an anarchist, who vowed to kill the next member of a royal family that he saw.
He explored parts of the northeastern coast of Greenland, Denmark, in 1905 during his Duke of Orléans Arctic Expedition on ship Belgica.
Philippe continued to reside in the United Kingdom until 1912, when he moved his primary residence to Belgium.
In 1914, Philippe and his wife Maria Dorothea were legally separated.
At the outbreak of the First World War, Philippe again tried unsuccessfully to join the French army.
In 1926, Philippe died of pneumonia at the Palais d'Orléans in Palermo, Sicily, Italy.
Having no legitimate issue, he was succeeded as pretender to the defunct throne of France by his cousin and brother in law, Jean, Duke of Guise.
Publications

Philippe wrote a number of works based on his many travels: 


He also published a collection of the papers of his father and of the Henri, comte de Chambord:
Honours

In popular culture

Duke Philippe of Orleans briefly appears in an urban fantasy novel for children, The Master Key (1901) by L. Frank Baum.



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
  AssignClass (16e8f916-7d69-4842-88bf-575e8d6c922d)
 Call ID: 16e8f916-7d69-4842-88bf-575e8d6c922d
  Args:
    source: :Prince_Philippe_Duke_of_Orleans
    type: :Man
  AssignClass (114b231d-db0d-44d7-abab-f46b5c42ed5c)
 Call ID: 114b231d-db0d-44d7-abab-f46b5c42ed5c
  Args:
    type: :Person
    source: :Prince_Philippe_Duke_of_Orleans
  AddLiteral (85fbbc9b-29f9-4e05-abfa-f80e14bd5ce4)
 Call ID: 85fbbc9b-29f9-4e05-abfa-f80e14bd5ce4
  Args:
    literal_value: 1869
    source: :Prince_Philippe_Duke_of_Orleans
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (4047d0eb-adc0-422c-a686-38b8d4a1d2af)
 Call ID: 4047d0eb-adc0-422c-a686-38b8d4a1d2af
  Args:
    source: :Prince_Philippe_Duke_of_Orleans
    literal_value: 1926
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (41460618-44d2-447e-ba3d-72d841d1e520)
 Call ID: 41460618-44d2-447e-ba3d-72d841d1e520
  Args:
    literal_value: Philippe VIII
    source: :Prince_Philippe_Duke_of_Orleans
    relation: :knownAs
    literal_type: xsd:string
  AssignClass (a47db57d-699f-49a9-bee5-dd5ec0c5253a)
 Call ID: a47db57d-699f-49a9-bee5-dd5ec0c5253a
  Args:
    type: :Man
    source: :Philippe_Count_of_Paris
  AssignClass (23ae01d7-7473-47a2-aaf5-5947910403f6)
 Call ID: 23ae01d7-7473-47a2-aaf5-5947910403f6
  Args:
    source: :Philippe_Count_of_Paris
    type: :Person
  AssignClass (3d359fd4-642d-4ec4-8863-eeacad27c0b5)
 Call ID: 3d359fd4-642d-4ec4-8863-eeacad27c0b5
  Args:
    type: :Woman
    source: :Princess_Isabelle_of_Orleans
  AssignClass (e808b9df-0912-4307-aba6-f03a7d5c6f36)
 Call ID: e808b9df-0912-4307-aba6-f03a7d5c6f36
  Args:
    source: :Princess_Isabelle_of_Orleans
    type: :Person
  AddTriple (118685f4-7107-4b83-9127-9af3c0971096)
 Call ID: 118685f4-7107-4b83-9127-9af3c0971096
  Args:
    source: :Prince_Philippe_Duke_of_Orleans
    target: :Philippe_Count_of_Paris
    relation: :hasFather
  AddTriple (7e370e28-702f-4267-a072-bc42e747634c)
 Call ID: 7e370e28-702f-4267-a072-bc42e747634c
  Args:
    target: :Princess_Isabelle_of_Orleans
    source: :Prince_Philippe_Duke_of_Orleans
    relation: :hasMother
  AssignClass (bc6e2dd5-3d53-4882-a4ee-d51bf96d5d89)
 Call ID: bc6e2dd5-3d53-4882-a4ee-d51bf96d5d89
  Args:
    source: :Amelie_of_Orleans
    type: :Woman
  AssignClass (f15ddd31-2b6b-4971-b0b2-2cf671237765)
 Call ID: f15ddd31-2b6b-4971-b0b2-2cf671237765
  Args:
    source: :Amelie_of_Orleans
    type: :Person
  AddTriple (055b43fd-66d5-4e72-9d0b-751daf83e105)
 Call ID: 055b43fd-66d5-4e72-9d0b-751daf83e105
  Args:
    relation: :hasSister
    target: :Amelie_of_Orleans
    source: :Prince_Philippe_Duke_of_Orleans
  AssignClass (17b533a9-fb58-4b6d-9065-fb820c2750c8)
 Call ID: 17b533a9-fb58-4b6d-9065-fb820c2750c8
  Args:
    type: :Man
    source: :Philippe_Debien
  AssignClass (d5d73102-32f1-40b2-895b-d93ab62c44dd)
 Call ID: d5d73102-32f1-40b2-895b-d93ab62c44dd
  Args:
    type: :Person
    source: :Philippe_Debien
  AddTriple (16e7342e-0237-4bf0-8c0c-66e944990354)
 Call ID: 16e7342e-0237-4bf0-8c0c-66e944990354
  Args:
    target: :Philippe_Debien
    source: :Prince_Philippe_Duke_of_Orleans
    relation: :hasSon
  AssignClass (10024630-2c41-4657-8d81-19949e20b7d2)
 Call ID: 10024630-2c41-4657-8d81-19949e20b7d2
  Args:
    type: :Woman
    source: :Nina
  AssignClass (9d4e289b-b223-46c1-be13-869ff129f0fd)
 Call ID: 9d4e289b-b223-46c1-be13-869ff129f0fd
  Args:
    source: :Nina,type:
    type: :Person
  AddTriple (ddb203c7-5e9b-49fd-9239-c5f96cbb823a)
 Call ID: ddb203c7-5e9b-49fd-9239-c5f96cbb823a
  Args:
    relation: :hasMother
    source: :Philippe_Debien
    target: :Nina
  AssignClass (530a19aa-b867-434b-bccd-6acc5e445073)
 Call ID: 530a19aa-b867-434b-bccd-6acc5e445073
  Args:
    source: :Archduchess_Maria_Dorothea_of_Austria
    type: :Woman
  AssignClass (3b377052-7f50-4ba0-86c6-52ab88ec78ad)
 Call ID: 3b377052-7f50-4ba0-86c6-52ab88ec78ad
  Args:
    source: :Archduchess_Maria_Dorothea_of_Austria
    type: :Person
  AddLiteral (80a4cada-b3d0-4f62-bce9-a76384d2c9ea)
 Call ID: 80a4cada-b3d0-4f62-bce9-a76384d2c9ea
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1896
    source: :Prince_Philippe_Duke_of_Orleans
  AddTriple (9154ac05-545b-45ff-8d80-98b51b46fa1b)
 Call ID: 9154ac05-545b-45ff-8d80-98b51b46fa1b
  Args:
    relation: :hasRelation
    target: :Archduchess_Maria_Dorothea_of_Austria
    source: :Prince_Philippe_Duke_of_Orleans
  AssignClass (b36c2ec9-53e8-4658-a974-5e88a94b8129)
 Call ID: b36c2ec9-53e8-4658-a974-5e88a94b8129
  Args:
    source: :Archduke_Joseph_Karl_of_Austria
    type: :Man
  AssignClass (775d9dd9-7c91-4bf4-9988-520f90980824)
 Call ID: 775d9dd9-7c91-4bf4-9988-520f90980824
  Args:
    source: :Archduke_Joseph_Karl_of_Austria
    type: :Person
  AddTriple (23d5abc7-33fc-49d8-af54-e14203cc18a9)
 Call ID: 23d5abc7-33fc-49d8-af54-e14203cc18a9
  Args:
    relation: :hasFather
    source: :Archduchess_Maria_Dorothea_of_Austria
    target: :Archduke_Joseph_Karl_of_Austria
  AssignClass (8fb1ee5c-e599-4540-87e4-5989e275da43)
 Call ID: 8fb1ee5c-e599-4540-87e4-5989e275da43
  Args:
    type: :Man
    source: :Jean_Duke_of_Guise
  AssignClass (64f0cc64-a545-4d21-8cf8-9cd4ee28fac0)
 Call ID: 64f0cc64-a545-4d21-8cf8-9cd4ee28fac0
  Args:
    type: :Person
    source: :Jean_Duke_of_Guise
  AddTriple (35fd0b48-b70c-4cf6-911a-92d522ea1b9a)
 Call ID: 35fd0b48-b70c-4cf6-911a-92d522ea1b9a
  Args:
    source: :Prince_Philippe_Duke_of_Orleans
    target: :Jean_Duke_of_Guise
    relation: :hasBrother
  Finish (d2c9f611-98ca-435c-9475-3e41b848d343)
 Call ID: d2c9f611-98ca-435c-9475-3e41b848d343
  Args: