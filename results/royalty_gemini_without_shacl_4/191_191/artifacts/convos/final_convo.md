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
Princess Hélène of Orléans (French: Princesse Hélène Louise Henriette d'Orléans; 13 June 1871 – 21 January 1951) was a member of the deposed Orléans royal family of France and, by marriage to the head of a cadet branch of the Italian royal family, the Duchess of Aosta.
Family

Hélène was the third of eight children born to Prince Philippe, Count of Paris, and Infanta Maria Isabel of Spain.
Her father was a grandson of Louis Philippe I, King of the French, and had been heir-apparent to the throne from 1842 until the exile of the dynasty in 1848.
Repatriating to France at the end of June 1871, the family took up residence in Paris at the Hotel Fould on the Rue du Faubourg Saint-Honoré, as guests of their uncle, Henri, Duke of Aumale, whose wealth and properties in France had not been confiscated in 1852, unlike those of the other Orléans princes.
On 21 December 1872 the National Assembly enacted a law of restitution, authorising restoration of approximately 40 million of the eighty million francs worth of property which had formerly belonged to the House of Orléans, although the actual re-acquisition of that wealth would take several years.
Meanwhile, a close friend of the Count and Countess of Paris, Maria Brignole Sale De Ferrari, placed at their disposal the ground floor and gardens of the Hôtel Matignon on the rue de Varenne in Paris.
Along the adjacent rue de Babylone the Duchess had a two-story town house built to accommodate the Orléans children, their governesses and tutors, which served as Hélène's home from 1876 until her father was again exiled.
In 1883 the last legitimate prince in the male-line of Louis XV, Henri, Count of Chambord, died childless leaving, in the eyes of French royalists excepting recalcitrant legitimists, the Count of Paris as heir to the Bourbon crown of France.
However, celebrations in Paris in the spring of 1886 prior to the marriage in Lisbon of Hélène's eldest sister Amélie to Carlos of Braganza-Coburg, Prince Royal of Portugal, evoked such clear expressions of monarchist support for the House of Orléans that on 22 July the French Republic took the precaution of banishing the heads of France's former ruling dynasties, the Orléans and Bonapartes, from the country.
Nearly all of the Orléans promptly left France, with Hélène and her parents going on to visit Tunbridge Wells in England and then travelling to Scotland before taking up residence in October at Sheen House in East Sheen, England.
Potential matches

Most of Hélène's siblings had married well, including Amélie, Queen of Portugal, Philippe, Duke of Orléans (who married Archduchess Maria Dorothea of Austria) and Isabelle, Duchess of Guise, and Hélène's parents had hopes that she would marry an heir to a throne.
Those hopes were fanned by the fact that Hélène was considered a great beauty for the day, and one contemporary source stated that she was "the personification of womanly health and beauty, distinguished as a graceful athlete and charming linguist".
Relationship with the Duke of Clarence

Prince Albert Victor, Duke of Clarence and Avondale ("Eddy") was the eldest son of the future Edward VII and grandson of then reigning Queen Victoria.
During the spring and summer of 1890, Eddy and Hélène were allowed to become acquainted at the homes of Clarence's sister Princess Louise, Duchess of Fife in Sheen and in Scotland, and, with the encouragement of their mothers, Hélène and Eddy fell in love.
On 29 August, Clarence obtained permission to meet alone with his grandmother at Balmoral Castle in Scotland, and brought Hélène with him.
Marriage to a Catholic would have entailed constitutional forfeiture of Eddy's claim to the British throne, pursuant to the Act of Settlement, but Hélène offered to become an Anglican.
When Queen Victoria expressed surprise at Hélène's offer, Hélène wept and insisted that her willingness to do so was for the sake of love.
This included her expectation that Hélène's father would not consent to his daughter's change of faith.
Hélène's father refused to countenance the marriage, was adamant she could not convert and informed the Queen of his decision.
He granted permission, nonetheless, for Hélène to personally beseech Pope Leo XIII for a dispensation to marry Clarence, but the Pope confirmed her father's verdict and the courtship ended.
Clarence never got over his feelings for Hélène and their relationship is commemorated at his tomb at Windsor Castle by a bead wreath with the single word "HELENE" written upon it.
Queen Victoria wrote to her grandson recommending another of her grandchildren, Princess Margaret of Prussia, as an alternative, but nothing came of that suggestion, and Clarence told his grandmother that his love for another cousin, Alix of Hesse (a match for which the Queen had long hoped) had gone unrequited.
An engagement to Princess Mary of Teck was later arranged, but Clarence died before their wedding could take place.
Although acknowledging his parents' desires for a French alliance in his diary, the future Tsar Nicholas II of Russia (a first cousin of Clarence) never pursued their choice, Hélène, as he was already in love with the aforementioned Alix of Hesse and secured their permission to marry her in 1894.
In 1892, while travelling in Egypt with her brother Philippe, Hélène met Ernst Gunther, Duke of Schleswig-Holstein, who decided that he would marry her, to the fury of his sister, the German Empress Augusta Victoria.
German diplomatic pressure put an end to Ernst Gunther's hopes, which were probably fruitless in any event as Hélène showed no interest in his advances.
In the meantime, he met his future wife, Countess Sophie Chotek, and never considered Hélène again.
Marriage and children

On 25 June 1895, at the Church of St. Raphael in Kingston upon Thames, Hélène married Prince Emanuele Filiberto of Savoy, 2nd Duke of Aosta (1869–1931).
The wedding was attended by Crown Prince Victor Emmanuel of Italy, the Prince and Princess of Wales and others of the British royal family.
The couple had two sons:


Widowed in 1931, Princess Hélène was married for a second time in 1936 to Colonel Otto Campini.
Avocations

In 1892 Hélène travelled with her brother Philippe to Egypt and Palestine, the first of many trips outside of Europe.
After the breakdown of both her health and her marriage, Hélène began frequent trips to Africa which lasted up to ten months at a time.
In 1913-1914 Hélène undertook a round-the-world trip which she recorded in another travel book.
War-time nurse

When the Italo-Turkish War broke out, Hélène trained as a nurse and went aboard the hospital ship Memfi, where she cared for wounded soldiers and those suffering from disease.
During World War I, Hélène became the head of the Italian Red Cross nurses and spent much of her time on or near the front lines.
For her service, Hélène was awarded the Italian Silver Medal for bravery, the Romanian Regina Maria Cross, the French Croix de Guerre, and the Insignia of a Dame Grand Cross of the Order of the British Empire.



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
  AssignClass (9bbec0ce-2f10-48e1-a801-c13354f4ed69)
 Call ID: 9bbec0ce-2f10-48e1-a801-c13354f4ed69
  Args:
    source: :Princess_Helene_of_Orleans
    type: :Woman
  AssignClass (0ac082b9-fece-450e-b8e1-d915aad3a0a4)
 Call ID: 0ac082b9-fece-450e-b8e1-d915aad3a0a4
  Args:
    source: :Princess_Helene_of_Orleans
    type: :Person
  AddLiteral (b748a7a4-cf23-4846-9503-e3280711c481)
 Call ID: b748a7a4-cf23-4846-9503-e3280711c481
  Args:
    literal_value: 1871
    relation: :hasBirthYear
    source: :Princess_Helene_of_Orleans
    literal_type: xsd:integer
  AddLiteral (49b2e005-2ce6-4ee4-bbb5-507f6e5a730f)
 Call ID: 49b2e005-2ce6-4ee4-bbb5-507f6e5a730f
  Args:
    literal_value: 1951
    relation: :hasDeathYear
    source: :Princess_Helene_of_Orleans
    literal_type: xsd:integer
  AssignClass (6c470884-fa71-4c80-b066-5635fa035c62)
 Call ID: 6c470884-fa71-4c80-b066-5635fa035c62
  Args:
    type: :Man
    source: :Prince_Philippe_Count_of_Paris
  AssignClass (266d5c42-a12b-4f7c-a280-1a60a25bd22c)
 Call ID: 266d5c42-a12b-4f7c-a280-1a60a25bd22c
  Args:
    type: :Person
    source: :Prince_Philippe_Count_of_Paris
  AssignClass (d685ad5d-2a7d-4f30-94b6-564e0c003a0e)
 Call ID: d685ad5d-2a7d-4f30-94b6-564e0c003a0e
  Args:
    source: :Infanta_Maria_Isabel_of_Spain
    type: :Woman
  AssignClass (325ee0b7-8f5c-468e-8ce3-82d6f81978f3)
 Call ID: 325ee0b7-8f5c-468e-8ce3-82d6f81978f3
  Args:
    type: :Person
    source: :Infanta_Maria_Isabel_of_Spain
  AddTriple (c7c7491e-ebc8-4c54-9259-7c88d5fd65ee)
 Call ID: c7c7491e-ebc8-4c54-9259-7c88d5fd65ee
  Args:
    source: :Princess_Helene_of_Orleans
    target: :Prince_Philippe_Count_of_Paris
    relation: :hasFather
  AddTriple (139158c1-1d48-43c0-be81-7553979f64af)
 Call ID: 139158c1-1d48-43c0-be81-7553979f64af
  Args:
    target: :Infanta_Maria_Isabel_of_Spain
    relation: :hasMother
    source: :Princess_Helene_of_Orleans
  AssignClass (fcf4d20b-f89c-44f5-ba7d-0df445a629e6)
 Call ID: fcf4d20b-f89c-44f5-ba7d-0df445a629e6
  Args:
    source: :Amelie_Queen_of_Portugal
    type: :Woman
  AssignClass (1a5885f5-4824-4d0a-84f7-7f9283a6ac25)
 Call ID: 1a5885f5-4824-4d0a-84f7-7f9283a6ac25
  Args:
    type: :Person
    source: :Amelie_Queen_of_Portugal
  AddTriple (62d11c9f-2f98-45c3-9011-4ed0cf91360d)
 Call ID: 62d11c9f-2f98-45c3-9011-4ed0cf91360d
  Args:
    source: :Amelie_Queen_of_Portugal
    target: :Princess_Helene_of_Orleans
    relation: :isSisterOf
  AssignClass (3d9128a6-decc-4fc9-91ab-46ec60a09736)
 Call ID: 3d9128a6-decc-4fc9-91ab-46ec60a09736
  Args:
    source: :Philippe_Duke_of_Orleans
    type: :Man
  AssignClass (53bc210b-760d-4073-8225-43a243200850)
 Call ID: 53bc210b-760d-4073-8225-43a243200850
  Args:
    source: :Philippe_Duke_of_Orleans
    type: :Person
  AddTriple (fc0f5c11-e6ef-4a24-b6a6-c1eadad39ed3)
 Call ID: fc0f5c11-e6ef-4a24-b6a6-c1eadad39ed3
  Args:
    relation: :isBrotherOf
    target: :Princess_Helene_of_Orleans
    source: :Philippe_Duke_of_Orleans
  AssignClass (7a99b37d-d504-4e8f-9ea1-d16c06b17d78)
 Call ID: 7a99b37d-d504-4e8f-9ea1-d16c06b17d78
  Args:
    type: :Woman
    source: :Isabelle_Duchess_of_Guise
  AssignClass (72823879-b162-43b0-b75c-41284fee1df9)
 Call ID: 72823879-b162-43b0-b75c-41284fee1df9
  Args:
    source: :Isabelle_Duchess_of_Guise
    type: :Person
  AddTriple (f9b955f6-eccc-4218-9ced-6c82b009adbd)
 Call ID: f9b955f6-eccc-4218-9ced-6c82b009adbd
  Args:
    target: :Princess_Helene_of_Orleans
    relation: :isSisterOf
    source: :Isabelle_Duchess_of_Guise
  AssignClass (08cc8149-d28f-4253-9336-283b32885f7d)
 Call ID: 08cc8149-d28f-4253-9336-283b32885f7d
  Args:
    type: :Man
    source: :Prince_Emanuele_Filiberto_of_Savoy_Duke_of_Aosta
  AssignClass (eb689f05-ca7f-45db-a860-9f9507429637)
 Call ID: eb689f05-ca7f-45db-a860-9f9507429637
  Args:
    source: :Prince_Emanuele_Filiberto_of_Savoy_Duke_of_Aosta
    type: :Person
  AddLiteral (0756e17a-cddd-4e3f-a39a-0680cd75dacd)
 Call ID: 0756e17a-cddd-4e3f-a39a-0680cd75dacd
  Args:
    literal_type: xsd:integer
    source: :Princess_Helene_of_Orleans
    relation: :hasMarriageYear
    literal_value: 1895
  AddTriple (099222a9-8db6-4d2a-8ca7-7c102101ce31)
 Call ID: 099222a9-8db6-4d2a-8ca7-7c102101ce31
  Args:
    target: :Prince_Emanuele_Filiberto_of_Savoy_Duke_of_Aosta
    relation: :hasRelation
    source: :Princess_Helene_of_Orleans
  AssignClass (aad8f651-1073-443f-971e-b0ce3d61f774)
 Call ID: aad8f651-1073-443f-971e-b0ce3d61f774
  Args:
    type: :Man
    source: :Colonel_Otto_Campini
  AssignClass (6631e1c4-3cfc-40c1-9497-98de77fa806f)
 Call ID: 6631e1c4-3cfc-40c1-9497-98de77fa806f
  Args:
    type: :Person
    source: :Colonel_Otto_Campini
  AddLiteral (2055e27f-7fed-4b94-8113-1d93350f69d9)
 Call ID: 2055e27f-7fed-4b94-8113-1d93350f69d9
  Args:
    source: :Princess_Helene_of_Orleans
    literal_type: xsd:integer
    literal_value: 1936
    relation: :hasMarriageYear
  AddTriple (56e794a0-36ef-4ff4-ace8-0495aac91dc7)
 Call ID: 56e794a0-36ef-4ff4-ace8-0495aac91dc7
  Args:
    source: :Princess_Helene_of_Orleans
    relation: :hasRelation
    target: :Colonel_Otto_Campini
  Finish (ef9c83f2-0ce8-4507-a63d-c1f6af14b61b)
 Call ID: ef9c83f2-0ce8-4507-a63d-c1f6af14b61b
  Args: