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
María de las Mercedes, Princess of Asturias (María de las Mercedes de Borbón y Habsburgo-Lorena; 11 September 1880 – 17 October 1904) was the eldest child of King Alfonso XII of Spain and his second wife, Maria Christina of Austria.
She was Princess of Asturias, the heiress presumptive to the Crown of Spain, for all 24 years of her life.
Had her younger sibling, unborn at the death of Alfonso XII, been a daughter, Mercedes would have been Queen of Spain.
The sibling proved to be a boy, Alfonso XIII, and upon his birth in 1886, he was King, and Mercedes turned out not to be queen.
She resumed the position of heiress presumptive, which she held until her own death (aged 24), and was succeeded in it by her own infant son Alfonso, Alfonso XIII having not yet married and fathered a legitimate child.
Mercedes married in Madrid on 14 February 1901, her second cousin, Prince Carlos of Bourbon-Two Sicilies, a nephew of the King of the then-defunct Kingdom of the Two Sicilies, who was elevated to the rank of Infante of Spain.
Early life

Born on 11 September 1880 at the Royal Palace of Madrid, Mercedes was the first child of King Alfonso XII and his second wife, Maria Christina of Austria.
She was christened María de las Mercedes Isabel Teresa Cristina Alfonsa.
To smooth things out, Queen Maria Christina suggested giving their new daughter the name Mercedes in honor of her husband's first wife and Queen, Mercedes of Orléans.
Mercedes was heiress presumptive at birth, but the disappointment was so great that she was initially treated only as an infanta.
Antonio Cánovas del Castillo, then head of the government, who disliked Maria Christina and did not want the crown to pass again to a female after the disastrous reign of Isabella II, decided functionally to ignore the newborn.
Mercedes's paternal aunt Isabella retained the title of Princess of Asturias until Práxedes Mateo Sagasta, President of the government that had replaced Cánovas, pressured King Alfonso XII to accord the title to Mercedes, which he did on 10 March 1881.
On 12 November 1882, Mercedes gained a sister, Infanta Maria Teresa.
Alfonso had married Maria Christina in order to secure the succession to the throne.
In July 1883, Maria Christina left the Spanish court and traveled with her daughters to visit her own family in Austria.
By the summer of 1884, Alfonso XII's health had deteriorated: he had tuberculosis.
Given the nascent pregnancy, Mercedes was not declared queen because she would be displaced if a son was born — instead, there was a six month interregnum until the birth of her brother Alfonso XIII on 17 May 1886, who assumed the throne as king immediately upon birth.
Had the pregnancy been lost or resulted in another daughter, Mercedes would have been declared queen regnant and been retroactively recognized as having assumed the throne at the death of her father (there would have been no interregnum).
Instead, with the late king's new issue arriving, and being a boy, Mercedes resumed the position of heiress presumptive, a title she would continue to hold for the rest of her short life.
Education

Mercedes made her first public appearance at the royal court by the hand of her mother when Queen Maria Christina was declared regent.
The education of the Princess of Asturias and her younger sister Infanta Maria Teresa was confined to the Royal Palace of Madrid in an austere environment headed by two widows: their mother and their paternal aunt Isabella (herself formerly Princess of Asturias).
Despite her constitutional status, Mercedes was not given an education that would have prepared her to govern the nation.
Mercedes grew up to be a serious young woman, shy and unprepossessing.
In her adolescence, Mercedes accompanied her mother on trips abroad visiting her paternal grandmother in Paris, her paternal aunt Paz in Munich, and her maternal grandmother Elisabeth Franziska in Vienna.
The situation in Spain became more complicated with the Spanish–American War in 1898.
Mercedes and her sister lived a restricted life.
At the dance, Mercedes fell in love with her cousin Prince Carlos of Bourbon-Two Sicilies, and the two were frequently seen together.
Marriage

Prince Carlos, Queen Maria Christina's first cousin once removed, belonged to the deposed royal family of the Two Sicilies and had arrived in Spain years earlier in order to follow a military career in the Spanish army.
The pairing of the princess and Prince Carlos was not accidental.
He had been chosen as a prospective husband by both Queen Maria Christina and Infanta Isabella, who was his aunt as well.
It was considered paramount to marry Mercedes to a member of the Bourbon family in order to avoid a change of the dynasty in case she succeeded her brother.
Prince Carlos offered other advantages as groom to the Princess of Asturias.
As he did not belong to a reigning royal family, he could settle permanently in Spain and adopt the necessary Spanish nationality.
Carlos was of serious character, shy, handsome, and Mercedes was attracted to him.
It was feared that Caserta's son marrying Mercedes would bring the Carlist party too close to the Spanish throne.
Even the Prince's name – Carlos – aroused suspicion.
There were bitter attacks against Mercedes's marriage in the newspapers and protest on the streets in Madrid, Seville and Granada.
The Archbishop of Valladolid, one of Spain’s most prominent prelates, wrote a letter to the Queen warning her against the dire consequences if the marriage would take place.
Mercedes herself expressed her frustration to the strong opposition to her choice of groom in a letter to her aunt Paz: "I am happy to marry him, but I am also upset at those who have created such a fuss and made mother suffer for this... all because his father fought alongside don Carlos.
Death

The couple lived at the Royal Palace of Madrid in close proximity to Queen Maria Christina, who wished for such proximity.
The union was happy and two children were born in quick succession: Prince Alfonso (1901–1964) and Prince Fernando (1903–1905).
Pregnant for the third time, Mercedes longed for a daughter after having two sons.
The following month, twenty days before her due day, Mercedes fell seriously ill.
Peritonitis set in and on the early hours on 16 October 1904 Mercedes gave birth prematurely to her third child, Princess Isabella Alfonsa (1904–1985).
The health of the mother was so seriously compromised that little attention was given to the child, who was believed to have been stillborn until the young King Alfonso realized the baby was alive.
Mercedes died the following day, on 17 October 1904, surrounded by her family.
Mercedes' three children were left in the care of Queen Maria Christina and raised in the court of King Alfonso XIII.
The elder son was not given the title of Prince of Asturias, but replaced his mother as heir presumptive.



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
  AssignClass (33da13cc-f300-43b8-81fa-68a536ba03e1)
 Call ID: 33da13cc-f300-43b8-81fa-68a536ba03e1
  Args:
    source: Maria_de_las_Mercedes
    type: :Woman
  AssignClass (a14dde06-c35b-4db3-b9bb-db28eff5436d)
 Call ID: a14dde06-c35b-4db3-b9bb-db28eff5436d
  Args:
    source: Maria_de_las_Mercedes
    type: :Person
  AddLiteral (ef6ea75f-019a-46c2-aaa4-8b87527aace9)
 Call ID: ef6ea75f-019a-46c2-aaa4-8b87527aace9
  Args:
    source: Maria_de_las_Mercedes
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1880
  AddLiteral (20172a41-8fa3-40c5-bd4b-b20d283c13bd)
 Call ID: 20172a41-8fa3-40c5-bd4b-b20d283c13bd
  Args:
    literal_type: xsd:integer
    source: Maria_de_las_Mercedes
    literal_value: 1904
    relation: :hasDeathYear
  AssignClass (c2c95701-8eaf-4597-9466-960037895f0c)
 Call ID: c2c95701-8eaf-4597-9466-960037895f0c
  Args:
    source: Alfonso_XII
    type: :Man
  AssignClass (528a409d-88d3-441d-b740-6a4d7aa3f4fc)
 Call ID: 528a409d-88d3-441d-b740-6a4d7aa3f4fc
  Args:
    type: :Person
    source: Alfonso_XII
  AssignClass (3f321585-3b79-4967-b1d1-4c0706e0f7d6)
 Call ID: 3f321585-3b79-4967-b1d1-4c0706e0f7d6
  Args:
    type: :Woman
    source: Maria_Christina_of_Austria
  AssignClass (e44e1689-16d8-4bd0-b53d-81ddd4a926e6)
 Call ID: e44e1689-16d8-4bd0-b53d-81ddd4a926e6
  Args:
    source: Maria_Christina_of_Austria
    type: :Person
  AddTriple (2211b6aa-cbc2-48e2-8aa9-3bffab489bc1)
 Call ID: 2211b6aa-cbc2-48e2-8aa9-3bffab489bc1
  Args:
    source: Maria_de_las_Mercedes
    target: Alfonso_XII
    relation: :hasFather
  AddTriple (9a9e6f21-0b2b-499d-8611-b37bc7ef0155)
 Call ID: 9a9e6f21-0b2b-499d-8611-b37bc7ef0155
  Args:
    source: Maria_de_las_Mercedes
    target: Maria_Christina_of_Austria
    relation: :hasMother
  AssignClass (806599f6-5d96-4328-92a3-5bae0aec9b4a)
 Call ID: 806599f6-5d96-4328-92a3-5bae0aec9b4a
  Args:
    source: Alfonso_XIII
    type: :Man
  AssignClass (27189ff1-a068-4ea3-b73a-abff66a5a9d5)
 Call ID: 27189ff1-a068-4ea3-b73a-abff66a5a9d5
  Args:
    type: :Person
    source: Alfonso_XIII
  AddTriple (8061ac5d-014a-4a81-814f-e85075e90af4)
 Call ID: 8061ac5d-014a-4a81-814f-e85075e90af4
  Args:
    target: Alfonso_XII
    relation: :hasFather
    source: Alfonso_XIII
  AddTriple (9a0322c1-2bd2-42c7-a087-71fc080bfc9e)
 Call ID: 9a0322c1-2bd2-42c7-a087-71fc080bfc9e
  Args:
    source: Alfonso_XIII
    relation: :hasMother
    target: Maria_Christina_of_Austria
  AssignClass (46e04390-bcaf-44e5-9913-eb365d67b145)
 Call ID: 46e04390-bcaf-44e5-9913-eb365d67b145
  Args:
    source: Infanta_Maria_Teresa
    type: :Woman
  AssignClass (f81ff6e5-ff96-4f79-ad69-83bccbdd7946)
 Call ID: f81ff6e5-ff96-4f79-ad69-83bccbdd7946
  Args:
    type: :Person
    source: Infanta_Maria_Teresa
  AddTriple (83a47f7e-72aa-4cb5-b840-0b674e2622c8)
 Call ID: 83a47f7e-72aa-4cb5-b840-0b674e2622c8
  Args:
    source: Infanta_Maria_Teresa
    target: Alfonso_XII
    relation: :hasFather
  AddTriple (0176cd20-d91a-4477-a816-e2667b0ad029)
 Call ID: 0176cd20-d91a-4477-a816-e2667b0ad029
  Args:
    relation: :hasMother
    target: Maria_Christina_of_Austria
    source: Infanta_Maria_Teresa
  AssignClass (d84a6a46-058e-4ce7-99aa-283ec0cbf89e)
 Call ID: d84a6a46-058e-4ce7-99aa-283ec0cbf89e
  Args:
    type: :Man
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AssignClass (e3d0a02a-6a2a-46ba-a50b-7cfde248c3b0)
 Call ID: e3d0a02a-6a2a-46ba-a50b-7cfde248c3b0
  Args:
    type: :Person
    source: Prince_Carlos_of_Bourbon-Two_Sicilies
  AddTriple (b62ac020-4bac-4ca6-aea7-075febfa2351)
 Call ID: b62ac020-4bac-4ca6-aea7-075febfa2351
  Args:
    source: Maria_de_las_Mercedes
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (c95dfac6-084f-49fd-b719-3d2164725917)
 Call ID: c95dfac6-084f-49fd-b719-3d2164725917
  Args:
    literal_type: xsd:integer
    source: Maria_de_las_Mercedes
    literal_value: 1901
    relation: :hasMarriageYear
  AssignClass (e5e5670d-0645-4704-bdab-c6dc0b4eadaf)
 Call ID: e5e5670d-0645-4704-bdab-c6dc0b4eadaf
  Args:
    source: Prince_Alfonso
    type: :Man
  AssignClass (1bfa6be1-2ca3-49b7-97ef-9bb6523dacdb)
 Call ID: 1bfa6be1-2ca3-49b7-97ef-9bb6523dacdb
  Args:
    type: :Person
    source: Prince_Alfonso
  AddTriple (1965f49e-ac3f-497c-a0b4-3fcc0e0830c9)
 Call ID: 1965f49e-ac3f-497c-a0b4-3fcc0e0830c9
  Args:
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    relation: :hasFather
    source: Prince_Alfonso
  AddTriple (f236bbb3-ec8d-4c65-acce-ee1fa3776058)
 Call ID: f236bbb3-ec8d-4c65-acce-ee1fa3776058
  Args:
    source: Prince_Alfonso
    target: Maria_de_las_Mercedes
    relation: :hasMother
  AssignClass (bcb57ecb-6158-4ef8-aab2-d1e5e46b92e7)
 Call ID: bcb57ecb-6158-4ef8-aab2-d1e5e46b92e7
  Args:
    source: Prince_Fernando
    type: :Man
  AssignClass (2a857786-c4e7-4e26-94ac-b84128614b19)
 Call ID: 2a857786-c4e7-4e26-94ac-b84128614b19
  Args:
    source: Prince_Fernando
    type: :Person
  AddTriple (e27173ce-f03d-4c67-baf2-25f112170bc5)
 Call ID: e27173ce-f03d-4c67-baf2-25f112170bc5
  Args:
    relation: :hasFather
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    source: Prince_Fernando
  AddTriple (e2d2edc2-c04c-44ad-b3ea-a90777e04834)
 Call ID: e2d2edc2-c04c-44ad-b3ea-a90777e04834
  Args:
    source: Prince_Fernando
    relation: :hasMother
    target: Maria_de_las_Mercedes
  AssignClass (4643d8ee-41a9-497e-ab32-831a0b0f5090)
 Call ID: 4643d8ee-41a9-497e-ab32-831a0b0f5090
  Args:
    type: :Woman
    source: Princess_Isabella_Alfonsa
  AssignClass (c22a65b3-ea6f-4382-aa54-37dafb1b935a)
 Call ID: c22a65b3-ea6f-4382-aa54-37dafb1b935a
  Args:
    source: Princess_Isabella_Alfonsa
    type: :Person
  AddTriple (a058dd9e-6c59-4bf2-ae37-5ca650959d46)
 Call ID: a058dd9e-6c59-4bf2-ae37-5ca650959d46
  Args:
    relation: :hasFather
    target: Prince_Carlos_of_Bourbon-Two_Sicilies
    source: Princess_Isabella_Alfonsa
  AddTriple (a8c35962-27ee-4ba6-a41e-d8219d0def11)
 Call ID: a8c35962-27ee-4ba6-a41e-d8219d0def11
  Args:
    source: Princess_Isabella_Alfonsa
    target: Maria_de_las_Mercedes
    relation: :hasMother
  Finish (b553ce8b-9cde-4426-9a68-1d2caf321109)
 Call ID: b553ce8b-9cde-4426-9a68-1d2caf321109
  Args: